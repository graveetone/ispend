import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function AuthReceiver() {
  const nav = useNavigate();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");
    if (token) {
      localStorage.setItem("ispend_token", token);
    }
    nav("/");
  }, []);
}
