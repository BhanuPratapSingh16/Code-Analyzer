import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import DashboardLayout from "../components/layout/DashboardLayout";
import { getRepoById } from "../services/repoService";
import "../styles/Repos.css";

export default function RepoDetails() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [repo, setRepo] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchRepo = async () => {
            try {
                setLoading(true);
                setError("");

                const data = await getRepoById(id);
                setRepo(data);
            } catch (err) {
                console.error("Failed to load repository:", err);
                setError(
                    err.response?.status === 404
                        ? "Repository not found."
                        : "Unable to load repository. Please try again."
                );
            } finally {
                setLoading(false);
            }
        };

        fetchRepo();
    }, [id]);

    if (loading) {
        return (
            <DashboardLayout>
                <div className="repos-empty">
                    <div className="loader"></div>
                    <p>Loading repository...</p>
                </div>
            </DashboardLayout>
        );
    }

    if (error || !repo) {
        return (
            <DashboardLayout>
                <div className="repos-empty">
                    <h2>{error || "Repository not found"}</h2>
                    <button
                        className="primary-button"
                        onClick={() => navigate("/repos")}
                    >
                        Back to repositories
                    </button>
                </div>
            </DashboardLayout>
        );
    }

    return (
        <DashboardLayout>
            <div className="repo-details-page">
                <button
                    className="repo-back-button"
                    onClick={() => navigate("/repos")}
                >
                    ← All repositories
                </button>

                <div className="repo-details-header">
                    <div className="repo-details-icon">{"</>"}</div>

                    <div className="repo-details-title">
                        <p className="repos-eyebrow">REPOSITORY WORKSPACE</p>
                        <h1>{repo.name}</h1>
                        <p>
                            {repo.description || "No description provided."}
                        </p>
                    </div>
                </div>

                <div className="repo-details-content">
                    <section className="repo-info-card">
                        <h2>Repository information</h2>

                        <div className="repo-info-row">
                            <span>Repository name</span>
                            <strong>{repo.name}</strong>
                        </div>

                        <div className="repo-info-row">
                            <span>Repository ID</span>
                            <strong>{repo.id}</strong>
                        </div>

                        <div className="repo-info-row">
                            <span>Description</span>
                            <strong>
                                {repo.description || "Not provided"}
                            </strong>
                        </div>

                        {repo.createdAt && (
                            <div className="repo-info-row">
                                <span>Created</span>
                                <strong>
                                    {new Date(repo.createdAt).toLocaleDateString()}
                                </strong>
                            </div>
                        )}
                    </section>

                    <section className="repo-next-step-card">
                        <div className="repo-next-step-icon">✦</div>
                        <h2>Ready to analyze your codebase?</h2>
                        <p>
                            Upload your project ZIP file to let CodeGraph AI
                            explore your files, understand dependencies and
                            visualize your code structure.
                        </p>

                        <button
                            className="primary-button"
                            disabled
                            title="ZIP upload page will be added next"
                        >
                            Upload ZIP — Coming next
                        </button>
                    </section>
                </div>
            </div>
        </DashboardLayout>
    );
}