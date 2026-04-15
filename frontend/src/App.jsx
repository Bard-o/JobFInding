import { useState, useEffect } from "react";
import Header from "./components/Header.jsx";
import MessageCard from "./components/MessageCard.jsx";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/messages?limit=50")
      .then((res) => {
        if (!res.ok) throw new Error(`API error: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        setMessages(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <>
      <Header />
      <main className="main-content">
        {loading && <p className="status-text">Loading messages...</p>}
        {error && <p className="status-text error">Error: {error}</p>}
        {!loading && !error && messages.length === 0 && (
          <p className="status-text">No messages found. Run the scraper first!</p>
        )}
        {messages.map((msg) => (
          <MessageCard key={msg.id} message={msg} />
        ))}
      </main>
    </>
  );
}

export default App;
