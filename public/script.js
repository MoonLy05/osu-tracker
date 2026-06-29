async function cargarUsuario() {
    try {
        const response = await fetch('/user');
        if (!response.ok) {
            throw new Error('Error al obtener los datos del usuario');
        }
        return await response.json();
    } catch (error) {
        console.error('Error al cargar el usuario:', error);
        return null;
    }
}

async function cargarDailyChallenges() {
    try {
        const response = await fetch('/daily_challenges');
        if (!response.ok) {
            throw new Error('Error al obtener los daily challenges');
        }
        return await response.json();
    } catch (error) {
        console.error('Error al cargar los daily challenges:', error);
        return [];
    }
}

async function cargarEstadisticas() {
    try {
        const response = await fetch('/stats');
        if (!response.ok) {
            throw new Error('Error al obtener las estadísticas');
        }
        return await response.json();
    } catch (error) {
        console.error('Error al cargar las estadísticas:', error);
        return [];
    }
}

function formatearFecha(valor) {
    if (!valor) {
        return 'Desconocida';
    }

    const fecha = new Date(valor);
    return Number.isNaN(fecha.getTime()) ? 'Desconocida' : fecha.toLocaleDateString('es-ES');
}

function escapeHtml(texto) {
    return String(texto)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function crearMetric(label, value, accent = false) {
    return `
        <div class="metric ${accent ? 'border border-pink-300/30' : ''}">
            <div class="label">${escapeHtml(label)}</div>
            <div class="value">${escapeHtml(value)}</div>
        </div>
    `;
}

async function actualizarDatos() {
    const datos = document.getElementById('datos');
    const usuario = await cargarUsuario();
    const dailyChallenges = await cargarDailyChallenges();
    const estadisticas = await cargarEstadisticas();

    if (!usuario) {
        datos.innerHTML = `
            <section class="loading-card flex items-center justify-center rounded-[2rem] p-6 text-center text-pink-100">
                No se pudieron cargar los datos del usuario.
            </section>
        `;
        return;
    }

    const avatarFallback = usuario.username?.charAt(0)?.toUpperCase() ?? '?';

    const dailyChallengesHTML = dailyChallenges.length
        ? dailyChallenges.map(dc => `
            <article class="daily-card p-5 sm:p-6">
                <div class="relative z-10">
                    <div class="mb-4 flex flex-wrap items-start justify-between gap-3">
                        <div>
                            <p class="eyebrow mb-2">daily challenge</p>
                            <h3 class="section-title text-2xl font-extrabold text-white">${formatearFecha(dc.momento)}</h3>
                        </div>
                        <span class="badge-soft text-sm font-semibold">${escapeHtml(dc.playcount)} plays</span>
                    </div>
                    <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
                        ${crearMetric('Daily actual', dc.daily_streak_current ?? '-')}
                        ${crearMetric('Daily best', dc.daily_streak_best ?? '-')}
                        ${crearMetric('Weekly actual', dc.weekly_streak_current ?? '-')}
                        ${crearMetric('Weekly best', dc.weekly_streak_best ?? '-')}
                        ${crearMetric('Top 10%', dc.top_10p_placements ?? '-')}
                        ${crearMetric('Top 50%', dc.top_50p_placements ?? '-')}
                    </div>
                </div>
            </article>
        `).join('')
        : `
            <div class="loading-card rounded-[2rem] p-6 text-center text-slate-200/80">
                Todavía no hay daily challenges guardados.
            </div>
        `;

    const filasStats = estadisticas.length
        ? estadisticas.map(stat => `
            <tr>
                <td class="font-semibold capitalize text-pink-100">${escapeHtml(stat.modo)}</td>
                <td>${stat.pp != null ? Number(stat.pp).toFixed(0) : '-'}</td>
                <td>${stat.global_rank ?? '-'}</td>
                <td>${stat.country_rank ?? '-'}</td>
                <td>${stat.nivel ?? '-'}</td>
                <td>${stat.accuracy != null ? (stat.accuracy * 100).toFixed(2) + '%' : '-'}</td>
                <td>${stat.play_count ?? '-'}</td>
                <td>${stat.play_time != null ? Math.round(stat.play_time / 3600) + 'h' : '-'}</td>
                <td>${stat.maximum_combo ?? '-'}</td>
            </tr>
        `).join('')
        : `<tr><td colspan="9" class="px-4 py-6 text-center text-slate-300/80">Sin estadísticas guardadas aún.</td></tr>`;

    datos.innerHTML = `
        <section class="card-glass overflow-hidden rounded-[2rem]">
            <div class="p-4 sm:p-6 lg:p-8">
                <img class="profile-banner mb-4" src="${usuario.cover_url}" alt="Cover de ${escapeHtml(usuario.username)}">
                <div class="flex flex-col gap-4 md:flex-row md:items-end">
                    ${usuario.avatar_url
                        ? `<img class="avatar" src="${usuario.avatar_url}" alt="Avatar de ${escapeHtml(usuario.username)}">`
                        : `<div class="avatar-fallback">${avatarFallback}</div>`
                    }
                    <div class="flex-1">
                        <div class="mb-2 flex flex-wrap items-center gap-3">
                            <h2 class="text-3xl font-black tracking-tight text-white sm:text-4xl">${escapeHtml(usuario.username)}</h2>
                            <span class="badge-soft text-sm font-semibold">${escapeHtml(usuario.country_code)}</span>
                        </div>
                        <p class="max-w-2xl text-sm text-slate-200/80 sm:text-base">
                            Soporte: ${usuario.is_supporter ? 'Sí' : 'No'} · Ha apoyado: ${usuario.has_supported ? 'Sí' : 'No'} · Registro: ${formatearFecha(usuario.join_date)}
                        </p>
                    </div>
                </div>
            </div>
            <div class="grid gap-3 px-4 pb-4 sm:grid-cols-2 xl:grid-cols-4 sm:px-6 lg:px-8 lg:pb-8">
                ${crearMetric('País', usuario.country_code ?? '-')}
                ${crearMetric('Soporte', usuario.is_supporter ? 'Sí' : 'No')}
                ${crearMetric('Ha apoyado', usuario.has_supported ? 'Sí' : 'No')}
                ${crearMetric('Ingreso', formatearFecha(usuario.join_date), true)}
            </div>
        </section>

        <section class="card-glass rounded-[2rem] p-4 sm:p-6 lg:p-8">
            <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
                <div>
                    <p class="eyebrow mb-2">estadísticas</p>
                    <h3 class="section-title text-2xl font-extrabold text-white">Rendimiento por modo</h3>
                </div>
                <span class="badge-soft text-sm font-semibold">${estadisticas.length} modos</span>
            </div>
            <div class="table-shell overflow-x-auto">
                <table>
                    <thead>
                        <tr>
                            <th>Modo</th>
                            <th>PP</th>
                            <th>Rango Global</th>
                            <th>Rango País</th>
                            <th>Nivel</th>
                            <th>Precisión</th>
                            <th>Juegos</th>
                            <th>Tiempo</th>
                            <th>Combo Máximo</th>
                        </tr>
                    </thead>
                    <tbody>${filasStats}</tbody>
                </table>
            </div>
        </section>

        <section>
            <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
                <div>
                    <p class="eyebrow mb-2">daily challenges</p>
                    <h3 class="section-title text-2xl font-extrabold text-white">Actividad diaria y semanal</h3>
                </div>
                <span class="badge-soft text-sm font-semibold">historial reciente</span>
            </div>
            <div class="grid gap-4">${dailyChallengesHTML}</div>
        </section>
    `;
}

document.addEventListener('DOMContentLoaded', () => {
    actualizarDatos();
});
