export default function Login() {
    const login = () => {
      window.location.href = `${import.meta.env.VITE_BACKEND_URL}/api/v1/oauth/login/google`;
    };

    function AuthButton({icon, caption, onClick}) {
        return (
            <button onClick={onClick} className="flex flex-col justify-center items-center p-3 bg-black text-white rounded-lg hover:bg-red-500 border border-2 border-red-500">
                <span>{icon}</span>
                <span>{caption}</span>
            </button>
        )
    }

    return (
        <div className="flex flex-col gap-5 m-10">
            <AuthButton icon="G" onClick={login} caption="Sign in with Google"/>
        </div>
    )
  }