import React, { useState } from 'react';
import './App.css'; // Import the CSS file

// Import images directly from the src directory
import rockImage from './rr.png';
import paperImage from './pp.png';
import scissorsImage from './ss.png';

const choices = {
  rock: rockImage,
  paper: paperImage,
  scissors: scissorsImage,
};

const compareChoices = (userChoice, computerChoice) => {
  if (userChoice === computerChoice) {
    return 'Tie';
  } else if (
    (userChoice === choices.rock && computerChoice === choices.scissors) ||
    (userChoice === choices.paper && computerChoice === choices.rock) ||
    (userChoice === choices.scissors && computerChoice === choices.paper)
  ) {
    return 'User';
  } else {
    return 'Computer';
  }
};

const RockPaperScissors = () => {
  const [userChoice, setUserChoice] = useState('');
  const [computerChoice, setComputerChoice] = useState('');
  const [result, setResult] = useState('');

  const handleClick = (choice) => {
    setUserChoice(choice);

    const choicesArray = Object.values(choices);
    const randomChoice = choicesArray[Math.floor(Math.random() * choicesArray.length)];
    setComputerChoice(randomChoice);

    const gameResult = compareChoices(choice, randomChoice);
    setResult(gameResult === 'Tie' ? "It's a tie!" : gameResult === 'User' ? 'You win!' : 'Computer wins!');
  };

  return (
    <div>
      <div id="photo">
        <div className="image-container">
          <img src={userChoice ? userChoice : ''} alt="User Choice" id="user-choice" />
        </div>
        <h2 id="result">{result}</h2>
        <div className="image-container">
          <img src={computerChoice ? computerChoice : ''} alt="Computer Choice" id="computer-choice" />
        </div>
      </div>

      <div className="choices">
        <img onClick={() => handleClick(choices.paper)} src={paperImage} alt="Paper" />
        <img onClick={() => handleClick(choices.rock)} src={rockImage} alt="Rock" />
        <img onClick={() => handleClick(choices.scissors)} src={scissorsImage} alt="Scissors" />
      </div>
    </div>
  );
};

export default RockPaperScissors;