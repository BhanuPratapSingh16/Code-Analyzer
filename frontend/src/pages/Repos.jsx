import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../components/layout/DashboardLayout";
import { getRepos } from "../services/repoService";
import "../styles/Repos.css";

export default function Repos() {
    const navigate = useNavigate();

    const [repos, setRepos] = useState([]);
    const [search, setSearch] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchRepos = async () => {
            try {
                const data = await getRepos();
                setRepos(Array.isArray(data) ? data : data.content || []);
            } catch (err) {
                console.error("Failed to load repositories:", err);
                setError("Unable to load repositories. Please try again.");
            } finally {
                setLoading(false);
            }
        };

        fetchRepos();
    }, []);

    const filteredRepos = repos.filter((repo) =>
        repo.name?.toLowerCase().includes(search.toLowerCase())
    );

    return (
        <DashboardLayout>
            <div className="repos-page">
                <div className="repos-page-heading">
                    <div>
                        <p className="repos-eyebrow">YOUR DEV WORKSPACE</p>
                        <h1>My Repositories</h1>
                        <p>Manage and explore all your code repositories.</p>
                    </div>

                    <button
                        className="primary-button"
                        onClick={() => navigate("/repos/new")}
                    >
                        + Create Repository
                    </button>
                </div>

                <div className="repos-toolbar">
                    <div className="repos-search">
                        <span>⌕</span>
                        <input
                            type="text"
                            placeholder="Search repositories..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>

                    <span className="repos-count">
                        {repos.length} repositories
                    </span>
                </div>

                {loading ? (
                    <div className="repos-empty">
                        <div className="loader"></div>
                        <p>Loading repositories...</p>
                    </div>
                ) : error ? (
                    <div className="repos-empty">
                        <p className="error-text">{error}</p>
                    </div>
                ) : filteredRepos.length === 0 ? (
                    <div className="repos-empty">
                        <div className="repos-empty-icon">{"</>"}</div>
                        <h2>
                            {repos.length === 0
                                ? "No repositories yet"
                                : "No matching repositories"}
                        </h2>
                        <p>
                            {repos.length === 0
                                ? "Create your first repository to get started."
                                : "Try searching with a different name."}
                        </p>

                        {repos.length === 0 && (
                            <button
                                className="primary-button"
                                onClick={() => navigate("/repos/new")}
                            >
                                Create your first repository
                            </button>
                        )}
                    </div>
                ) : (
                    <div className="all-repos-grid">
                        {filteredRepos.map((repo) => (
                            <article
                                className="all-repo-card"
                                key={repo.id}
                                onClick={() => navigate(`/repos/${repo.id}`)}
                                role="button"
                                tabIndex={0}
                                onKeyDown={(e) => {
                                    if (e.key === "Enter") {
                                        navigate(`/repos/${repo.id}`);
                                    }
                                }}
                            >
                                <div className="all-repo-card-top">
                                    <div className="all-repo-icon">
                                        {"</>"}
                                    </div>
                                    <span className="repo-open-arrow">↗</span>
                                </div>

                                <h3>{repo.name}</h3>

                                <p className="all-repo-description">
                                    {repo.description || "No description provided."}
                                </p>

                                <div className="all-repo-footer">
                                    <span>View repository</span>
                                    <span>→</span>
                                </div>
                            </article>
                        ))}
                    </div>
                )}
            </div>
        </DashboardLayout>
    );
}