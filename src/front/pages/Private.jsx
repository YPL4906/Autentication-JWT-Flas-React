import { useEffect, useState } from "react";

function Private() {
  const [message, setMessage] = useState("");
  const token = sessionStorage.getItem("token");

  const logout = () => {
    sessionStorage.removeItem("token");
    window.location.href = "/login";
  };

  useEffect(() => {
    if (!token) {
      window.location.href = "/login";
      return;
    }

    fetch(`${import.meta.env.VITE_BACKEND_URL}/private`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Unauthorized");
        return res.json();
      })
      .then((data) => setMessage(data.msg))
      .catch(() => {
        sessionStorage.removeItem("token");
        window.location.href = "/login";
      });
  }, [token]);

  return (
    <div>
      <h1>Private Page</h1>
      <p>{message}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}

export default Private;
