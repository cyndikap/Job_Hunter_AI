const jobs = [
  {
    id: 1,
    title: 'Data Engineer',
    company: 'Apex Data',
    location: 'Paris',
    score: 92,
    classification: 'Excellent Match',
    skills: ['Azure', 'Databricks', 'PySpark', 'Python'],
    url: 'https://candidat.apec.fr/offres-demploi/data-engineer-paris-12345',
  },
  {
    id: 2,
    title: 'AI Engineer',
    company: 'Nova AI',
    location: 'Remote',
    score: 88,
    classification: 'Strong Match',
    skills: ['GenAI', 'LLM', 'Python', 'Azure'],
    url: 'https://www.welcometothejungle.com/fr/jobs/ai-engineer-remote',
  },
]

const stats = [
  { label: 'Offres détectées', value: '128' },
  { label: 'Pertinentes', value: '42' },
  { label: 'Candidatures', value: '11' },
  { label: 'Temps moyen', value: '19 min' },
]

export default function HomePage() {
  return (
    <main className="mx-auto max-w-7xl p-6">
      <header className="mb-8 flex items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-brand-500">Job Hunter AI</p>
          <h1 className="mt-2 text-3xl font-bold">Veille emploi Data, IA & Cloud</h1>
        </div>
        <button className="rounded-xl bg-brand-600 px-4 py-2 font-semibold text-white hover:bg-brand-500">
          Lancer un scan
        </button>
      </header>

      <section className="mb-8 grid gap-4 md:grid-cols-4">
        {stats.map((stat) => (
          <div key={stat.label} className="card">
            <div className="text-sm text-slate-400">{stat.label}</div>
            <div className="mt-3 text-3xl font-bold">{stat.value}</div>
          </div>
        ))}
      </section>

      <section className="mb-8 card">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold">Meilleures opportunités</h2>
          <span className="text-sm text-slate-400">2 postes</span>
        </div>

        <div className="space-y-4">
          {jobs.map((job) => (
            <div key={job.id} className="rounded-xl border border-slate-700 bg-slate-950/50 p-4">
              <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                <div>
                  <h3 className="text-lg font-semibold">{job.title}</h3>
                  <p className="text-sm text-slate-400">{job.company}</p>
                </div>
                <div className="rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-sm font-medium text-emerald-300">
                  {job.score}% · {job.classification}
                </div>
              </div>

              <div className="mt-3 flex flex-wrap gap-2">
                {job.skills.map((skill) => (
                  <span key={skill} className="rounded-full bg-slate-800 px-2.5 py-1 text-xs text-slate-200">
                    {skill}
                  </span>
                ))}
              </div>

              <div className="mt-4 flex items-center justify-between text-sm text-slate-300">
                <span>{job.location}</span>
                <a href={job.url} target="_blank" rel="noreferrer" className="text-brand-500 hover:underline">
                  Voir l’offre
                </a>
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
