// habitos-frontend/src/DailyQuote.jsx

import React, { useState, useEffect } from 'react';

const DailyQuote = () => {
  const [quote, setQuote] = useState('');

  // Array of quotes corresponding to Sunday (0) through Saturday (6)
  const quotes = [
    "Every day is a new opportunity to do something.",
    "Life is what you make of it, so do something incredible.",
    "You can do it all.",
    "You are a masterpiece in the making.",
    "Don't forget to look at how far you have come.",
    "Not every day needs to be memorable. Keep at it, you got this!",
    "It's not about being perfect, it's about consistently showing up for yourself.",
  ];

  useEffect(() => {
    // Get the current day of the week (0 = Sunday, 1 = Monday, etc.)
    const dayIndex = new Date().getDay(); 
    setQuote(quotes[dayIndex]);
  }, []);

  return (
    <div className="quote-container">
      <blockquote>
        "{quote}"
      </blockquote>
    </div>
  );
};

export default DailyQuote;
