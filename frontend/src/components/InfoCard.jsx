// src/components/InfoCard.jsx
const InfoCard = ({ title, description }) => {
  return (
    <div className="info-card">
      <h3>{title}</h3>
      <p>{description}</p>
      <button className="read-more-btn">Read More</button>
    </div>
  );
};

export default InfoCard;
