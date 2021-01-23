package com.ussailing.rankings.unit.model.glicko2;

import org.junit.jupiter.api.Test;

import com.ussailing.rankings.model.glicko2.Player;
import com.ussailing.rankings.model.glicko2.RatingEngine;

public class RatingEngineTest {
	
	Player p1 = new Player("p","1");
	Player p2 = new Player("p","2");
	Player p3 = new Player("p","3",1200.0,RatingEngine.DEFAULT_DEVIATION,RatingEngine.DEFAULT_VOLATILITY);
	Player p4 = new Player("p","4",RatingEngine.DEFAULT_RATING,200.0,RatingEngine.DEFAULT_VOLATILITY);
	Player p5 = new Player("p","5",RatingEngine.DEFAULT_RATING,RatingEngine.DEFAULT_DEVIATION,0.01);
	
	// There was some chatter on the gh for the original application that there can
	// be a failure with convergence here
	@Test
	void testCalculateNewRating() {
		
	}
	
	@Test
	void testUpdateRatings() {
		
	}
	
}
