package com.ussailing.rankings.model;

import javax.persistence.Entity;
import javax.persistence.Table;

import com.ussailing.rankings.model.glicko2.Player;
import com.ussailing.rankings.model.glicko2.RatingEngine;
 
@Entity
@Table(name = "Sailor")
public class Sailor extends Player {
	
	private static final long serialVersionUID = -9070223475888842325L;

	public Sailor(String firstName, String lastName, RatingEngine ratingSystem) {
		super(firstName, lastName, ratingSystem);
	}
	
	public Sailor(String firstName, String lastName, Double initRating, Double initRatingDeviation,
			Double initVolatility) {
		super(firstName, lastName, initRating, initRatingDeviation, initVolatility);
	}

}
