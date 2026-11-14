import DashboardLayout from "../components/layout/DashboardLayout";
import { useEffect, useState } from "react";
import "../styles/Dashboard.css"
import { getRepos } from "../services/repoService";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
    const navigate = useNavigate();

    const [repos, setRepos] = useState([]);
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchRepos = async () => {
            try {
                setLoading(true)
                const data = await getRepos();

                setRepos(Array.isArray(data) ? data : data.content || [])
            }
            catch (err) {
                setError("Unable to load the repos!");
                console.error("Repos load fail ", err)
            }
            finally {
                setLoading(false)
            }
        }
        fetchRepos();
    }, [])

    return (
        <DashboardLayout>
            <section className="welcome-section">
                <div>
                    <p className="welcome-eyebrow">YOUR DEV WORKSPACE</p>
                    <h1>Welcome back <span>👋</span></h1>
                    <p className="welcome-description">
                        Understand your codebase. Visualize connections.
                        Build smarter software.
                    </p>
                </div>

                <button
                    className="primary-button"
                    onClick={() => navigate("/repos/new")}
                >
                    <span>＋</span> Create New repo
                </button>

            </section>

            <section className="repos-section">
                <div className="section-header">
                    <div>
                        <h2>Recent repos</h2>
                        <p>Manage and explore your code repositories</p>
                    </div>
                    <button className="secondary-button"
                        onClick={() => navigate("/repos")}
                    >
                        View all repos
                    </button>
                </div>

                {loading ? (
                    <div className="empty-panel">
                        <div className="loader"></div>
                        <p>Loading your repos...</p>
                    </div>
                ) : error ? (
                    <div className="empty-panel">
                        <p className="error-text">
                            {error}
                        </p>
                    </div>
                ) : repos.length === 0 ? (
                    <div className="empty-panel">
                        <div className="empty-icon">⌘</div>
                        <h3>No repos yet</h3>
                        <p>Create your first repo and upload your code ZIP to start exploring your codebase.</p>
                        <button className="primary-button" onClick={() => navigate("/repos/new")}>
                            + Create your first repo
                        </button>
                    </div>
                ) : (
                    <div className="repos-grid">
                        {repos.slice(0, 6).map((repo) => (
                            <article
                                className="repo-card"
                                key={repo.id}
                                onClick={() => navigate(`/repos/${repo.id}`)}
                                role="button"
                                tabIndex={0}
                            >
                                <div className="repo-card-top">
                                    <div className="repo-icon">{"</>"}</div>
                                </div>

                                <h3>{repo.name}</h3>

                                <div className="repo-card-footer">
                                    <span className="repo-arrow">↗</span>
                                </div>
                            </article>
                        ))}
                    </div>
                )
                }
            </section>
            <section className="quick-start">
                <div className="quick-start-icon">✦</div>
                <div>
                    <h3>Ready to understand your codebase?</h3>
                    <p>
                        Create a repo, upload your ZIP file, and let CodeGraph AI explore your code structure.
                    </p>
                </div>
                <button
                    className="secondary-button"
                    onClick={() => navigate("/repos/new")}
                >
                    Get started →
                </button>
            </section>
        </DashboardLayout>
    )
}
