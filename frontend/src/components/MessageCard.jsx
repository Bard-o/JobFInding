import "./MessageCard.css";

function MessageCard({ message }) {
  // Format dates to a readable string (e.g. "14/05/2026")
  const formatDate = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  return (
    <article className="message-card">
      {/* Top row: metadata table */}
      <div className="message-meta">
        <div className="meta-cell">
          <span className="meta-label">Message ID:</span>
          <span className="meta-value">{message.telegram_msg_id}</span>
        </div>
        <div className="meta-cell">
          <span className="meta-label">Sender ID</span>
          <span className="meta-value">{message.sender_id ?? "—"}</span>
        </div>
        <div className="meta-cell">
          <span className="meta-label">message date:</span>
          <span className="meta-value">{formatDate(message.message_date)}</span>
        </div>
        <div className="meta-cell">
          <span className="meta-label">created at</span>
          <span className="meta-value">{formatDate(message.created_at)}</span>
        </div>
      </div>

      {/* Bottom: text content */}
      <div className="message-body">
        <span className="body-label">Text content:</span>
        <p className="body-text">
          {message.text_content || "(no text content)"}
        </p>
      </div>
    </article>
  );
}

export default MessageCard;
