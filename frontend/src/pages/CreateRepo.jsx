import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../components/layout/DashboardLayout";
import { createRepo } from "../services/repoService";
import "../styles/CreateRepo.css";

export default function CreateRepo() {
    const navigate = useNavigate();
    
    const [repoName, setRepoName] = useState("")
    const [loading, setLoading] = useState("")
    const [error, setError] = useState("")

    const handleSubmit = async (e) => {
        e.preventDefault();

        if(!repoName.trim()){
            setError("Repository name is required");
            return;
        }

        try{
            setLoading(true);
            setError("");

            const repo = await createRepo({name: repoName.trim()});

            navigate(`/repos/${repo.id}`);
        }
        catch (err){
            setError(
                err.response?.data?.message ||
                err.response?.data?.error ||
                "Unable to create repository. Please try again."
            );
        }
        finally{
            setLoading(false);
        }
    }
    return (
        <DashboardLayout>
            <div className="create-repo-page">
                <button className="back-button" type="button" onClick={() => navigate("/dashboard")}>
                    ← Back to Dashboard
                </button>

                <div className="create-repo-heading">
                    <p className="create-repo-eyebrow">
                        YOUR DEV WORKSPACE
                    </p>
                    <h1>Create a new repository</h1>
                    <p>
                        Set up a workspace for your codebase. You can upload your ZIP file in the next step.
                    </p>
                </div>
                <div className="create-repo-card">
                    <div className="create-repo-icon">{"</>"}</div>

                    <h2>Repository details</h2>
                    <p className="create-repo-card-description">
                        Give your repository a name.
                    </p>

                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="repoName">Repository name <span>*</span></label>

                            <input id="repoName" type="text" value={repoName}
                                onChange={(e) => setRepoName(e.target.value)} maxLength={20} required
                            />
                        </div>
                        {error && (
                            <div className="create-repo-error">
                                {error}
                            </div>
                        )}

                        <div className="create-repo-actions">
                            <button type="button" className="cancel-button" onClick={() => navigate("/dashboard")} disabled={loading}>Cancel</button>
                            <button type="submit" className="primary-button" disabled={loading || !repoName.trim()}>{loading ? "Creating..." : "Create Repository"}</button>
                        </div>
                    </form>
                </div>
                <div className="create-repo-hint">
                    <span>✦</span>
                    <p>
                        After creating your repository, you'll be able to upload your code ZIP and start exploring its structure.
                    </p>
                </div>
            </div>
        </DashboardLayout>
    )
}