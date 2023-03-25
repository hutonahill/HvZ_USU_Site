import React from 'react'
import "./home.css"
import zombiesText from '../../images/HvZ-Text.png'
import henryImage from '../../images/henry-shot.jpg'

export default function Home() {
  return (
    <div className='home-background'>
      <div>
        <div className='about-us-wrapper'>
          <h1>The ZombieAggies Association</h1>
          <h2 className='about-us-text'>We're a USU RHA club dedicated to night games and fun on campus. Every semester, we play a week-long game of infection tag starting at 8AM and going until 10PM. Humans try to sneak between classes while avoiding Zombies who hunt and pursue their targets. Every night during this week, we meet and play different missions where the Zombies try to capture the Humans while the Humans try to thwart the Zombies.</h2>
        </div>
      </div>
      <div className='Presidency'>
        <h1>The Presidency</h1>
        <div className='person-wrapper'>
          <div className='Person'>
            <div className='sub-rectangle'>
              <h1 className='person-title'>Henry Riker</h1>
              <h2 className='person-sub-title'>President</h2>
            </div>
            <img className='headshot' src={henryImage}/>
          </div>
          <div className='Person'>
              <div className='sub-rectangle'>
              <h1 className='person-title'>Henry Riker</h1>
              <h2 className='person-sub-title'>Vice-President</h2>
            </div>
            <img className='headshot' src={henryImage}/>
          </div>
          <div className='Person'>
              <div className='sub-rectangle'>
              <h1 className='person-title'>Henry Riker</h1>
              <h2 className='person-sub-title'>Vice-President</h2>
            </div>
            <img className='headshot' src={henryImage}/>
          </div>
        </div>
      </div>
    </div>
  )
}
