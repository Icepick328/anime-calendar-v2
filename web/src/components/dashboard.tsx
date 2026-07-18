"use client";

import { useMemo, useState } from "react";
import { continueWatching, todayReleases, upcomingReleases } from "@/data/demo";

function Icon({ name }: { name: "calendar" | "play" | "clock" | "bell" | "sparkles" }) {
  const paths = {
    calendar: <><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 10h18"/></>,
    play: <path d="m8 5 11 7-11 7V5Z"/>,
    clock: <><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></>,
    bell: <><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/><path d="M10 21h4"/></>,
    sparkles: <><path d="m12 3-1.2 3.8L7 8l3.8 1.2L12 13l1.2-3.8L17 8l-3.8-1.2L12 3Z"/><path d="m5 14-.7 2.3L2 17l2.3.7L5 20l.7-2.3L8 17l-2.3-.7L5 14Z"/></>,
  };
  return <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">{paths[name]}</svg>;
}

function ReleaseRow({ release }: { release: (typeof todayReleases)[number] }) {
  return (
    <li className="release-row">
      <div className="time-pill">{release.time}</div>
      <div className="release-main">
        <strong>{release.title}</strong>
        <span>{release.episode} · {release.provider}</span>
      </div>
      <span className={`kind kind-${release.kind.toLowerCase()}`}>{release.kind}</span>
    </li>
  );
}

export function Dashboard() {
  const [scope, setScope] = useState<"Today" | "Week">("Today");
  const [demoNotice, setDemoNotice] = useState(true);
  const releaseCount = useMemo(() => scope === "Today" ? todayReleases.length : todayReleases.length + upcomingReleases.length, [scope]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark"><Icon name="calendar" /></span><span>Anime Calendar</span></div>
        <nav aria-label="Main navigation">
          <a className="nav-item active" href="#dashboard"><Icon name="sparkles" />Dashboard</a>
          <a className="nav-item" href="#releases"><Icon name="clock" />Releases</a>
          <a className="nav-item" href="#watching"><Icon name="play" />My Library</a>
          <a className="nav-item" href="#notifications"><Icon name="bell" />Notifications</a>
        </nav>
        <div className="sidebar-footer"><span className="avatar">B</span><div><strong>Demo Visitor</strong><span>Sample profile</span></div></div>
      </aside>

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <div><p className="eyebrow">Friday, July 17</p><h1>Good evening, Brad</h1><p>Your anime week, organized around what matters to you.</p></div>
          <div className="top-actions"><span className="demo-badge">Demo Mode</span><button type="button" className="primary-button">Create account</button></div>
        </header>

        {demoNotice && <section className="demo-callout" aria-live="polite"><div><Icon name="sparkles"/><div><strong>You’re exploring with sample data</strong><p>Create an account later to connect your watchlist, timezone, providers, and private calendar.</p></div></div><button type="button" onClick={() => setDemoNotice(false)} aria-label="Dismiss demo message">×</button></section>}

        <section className="metrics" aria-label="Dashboard summary">
          <div className="metric"><span>Releases today</span><strong>{todayReleases.length}</strong><small>2 dubs · 2 subs</small></div>
          <div className="metric"><span>Ready to watch</span><strong>{continueWatching.filter(item => item.available).length}</strong><small>Based on progress</small></div>
          <div className="metric"><span>Coming this week</span><strong>{todayReleases.length + upcomingReleases.length}</strong><small>Across 3 providers</small></div>
          <div className="metric"><span>Calendar status</span><strong className="status-value">Synced</strong><small>Updated 8 min ago</small></div>
        </section>

        <section className="dashboard-grid">
          <article className="panel releases-panel" id="releases">
            <div className="panel-heading"><div><p className="eyebrow">Release radar</p><h2>{scope === "Today" ? "Today’s releases" : "This week"}</h2></div><div className="segmented" aria-label="Release range"><button type="button" className={scope === "Today" ? "selected" : ""} onClick={() => setScope("Today")}>Today</button><button type="button" className={scope === "Week" ? "selected" : ""} onClick={() => setScope("Week")}>Week</button></div></div>
            <p className="panel-summary">{releaseCount} releases in your selected view</p>
            <ul className="release-list">{todayReleases.map((release) => <ReleaseRow key={`${release.title}-${release.episode}`} release={release} />)}{scope === "Week" && upcomingReleases.map((release) => <ReleaseRow key={`${release.title}-${release.episode}`} release={release} />)}</ul>
          </article>

          <article className="panel" id="watching">
            <div className="panel-heading"><div><p className="eyebrow">Your library</p><h2>Continue watching</h2></div><button type="button" className="text-button">View all</button></div>
            <div className="watching-list">{continueWatching.map(item => { const pct = Math.min(100, Math.round((item.progress / item.total) * 100)); return <div className="watching-item" key={item.title}><div className="poster-placeholder">{item.title.split(" ").slice(0,2).map(word => word[0]).join("")}</div><div className="watching-copy"><strong>{item.title}</strong><span>{item.nextEpisode} ready</span><div className="progress"><span style={{width: `${pct}%`}} /></div><small>{item.progress} of {item.total} episodes</small></div><button type="button" className="play-button" aria-label={`Play ${item.title}`}><Icon name="play"/></button></div>})}</div>
          </article>

          <article className="panel timeline-panel">
            <div className="panel-heading"><div><p className="eyebrow">Next 48 hours</p><h2>Release timeline</h2></div><span className="coming-soon">Preview</span></div>
            <div className="timeline"><span className="timeline-line" />{todayReleases.slice(0,3).map((release, index) => <div className="timeline-item" key={release.title}><span className="timeline-dot"/><time>{release.time}</time><div><strong>{release.title}</strong><span>{release.episode}</span></div>{index === 0 && <span className="next-label">Next</span>}</div>)}</div>
          </article>

          <article className="panel upcoming-panel">
            <div className="panel-heading"><div><p className="eyebrow">Plan ahead</p><h2>Coming up</h2></div><button type="button" className="text-button">Calendar</button></div>
            <ul className="upcoming-list">{upcomingReleases.map(release => <li key={release.title}><div><strong>{release.title}</strong><span>{release.episode}</span></div><time>{release.time}</time></li>)}</ul>
          </article>
        </section>
      </main>
    </div>
  );
}
