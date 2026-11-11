import "./App.css";
import AuthPage from "./pages/AuthPage";

function App() {
  return (
    <>
      <AuthPage
        onLogin={(data) => console.log("Login:", data)}
        onSignup={(data) => console.log("Signup:", data)}
      />
    </>
  )
}

export default App;
