/**
 * Copyright (c) 2020 as part of SailorRankings, All rights reserved.
 * @author Dan Birmingham. Please reach out to dgbirm@gmail.com
 * Date generated: Nov 7, 2020
 * @version jdk-11
 * 
 * ADAPTED DIRECTLY FROM:
 * 
 * Copyright (C) 2013 Jeremy Gooch <http://www.linkedin.com/in/jeremygooch/>
 *
 * The license covering the contents of this file is described in the file LICENCE.txt,
 * which should have been included as part of the distribution containing this file.
 */

package com.ussailing.rankings.model.glicko2;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Inheritance;
import javax.persistence.InheritanceType;
import javax.persistence.Table;
import javax.persistence.Transient;

import com.ussailing.rankings.model.Model;

/**
 * Holds an individual's Glicko-2 rating.
 *
 * <p>Glicko-2 ratings are an average skill value, a standard deviation and a volatility (how consistent the player is).
 * Prof Glickman's paper on the algorithm allows scaling of these values to be more directly comparable with existing rating
 * systems such as Elo or USCF's derivation thereof. This implementation outputs ratings at this larger scale.</p>
 *
 * @author Jeremy Gooch
 */

@Entity
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
@Table(name = "player")
public class Player implements Model, Serializable {

	/** The Constant serialVersionUID. */
	private static final long serialVersionUID = 7857123826265978286L; //default generated
	
	/** The id. */
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "idPlayer", updatable = false, nullable = false)
	private Long id;
	
	/** The first name. */
	@Column(name = "firstName", updatable = false, nullable = false, length = 30)
	private String firstName;
	
	/** The last name. */
	@Column(name = "lastName", updatable = false, nullable = false, length = 30)
	private String lastName;
	
	/** The rating. */
	@Column(name = "rating" , updatable = true, nullable = false)
	private Double rating;
	
	/** The rating deviation. */
	@Column(name = "ratingDeviation", updatable = true, nullable = false)
	private Double ratingDeviation;
	
	/** The volatility. */
	@Column(name = "volatility", updatable = true, nullable = false)
	private Double volatility;
	
	/** The number of results from which the rating has been calculated. */
	@Column(name = "volatility", updatable = true, nullable = false)
	private int numberOfResults = 0; 

	// the following variables are used to hold 
	// values temporarily whilst running calculations
	@Transient
	private Double workingRating;
	@Transient
	private Double workingRatingDeviation;
	@Transient
	private Double workingVolatility;
	
	/**
	 * Instantiates a new player.
	 *
	 * @param firstName    the first name.
	 * @param lastName     the last name.
	 * @param ratingSystem An instance of the RatingEngine object
	 */
	public Player(String firstName, String lastName, RatingEngine ratingSystem) {
		this.firstName = firstName;
		this.lastName = lastName;
		this.rating = ratingSystem.getDefaultRating();
		this.ratingDeviation = ratingSystem.getDefaultRatingDeviation();
		this.volatility = ratingSystem.getDefaultVolatility();
	}

	/**
	 * Instantiates a new player.
	 *
	 * @param firstName           the first name.
	 * @param lastName            the last name.
	 * @param initRating          the init rating
	 * @param initRatingDeviation the init rating deviation
	 * @param initVolatility      the init volatility
	 */
	public Player(String firstName, String lastName, Double initRating, Double initRatingDeviation, Double initVolatility) {
		this.firstName = firstName;
		this.lastName = lastName;
		this.rating = initRating;
		this.ratingDeviation = initRatingDeviation;
		this.volatility = initVolatility;
	}

	/**
	 * Return the rating value of the player.
	 * 
	 * @return Double
	 */
	public Double getRating() {
		return this.rating;
	}

	/**
	 * Sets the rating.
	 *
	 * @param rating the new rating
	 */
	public void setRating(Double rating) {
		this.rating = rating;
	}

	/**
	 * Return the average skill value of the player scaled down
	 * to the scale used by the algorithm's internal workings.
	 * 
	 * @return Double
	 */
	public Double getGlicko2Rating() {
		return RatingEngine.convertRatingToGlicko2Scale(this.rating);
	}

	/**
	 * Set the average skill value, taking in a value in Glicko2 scale.
	 *
	 * @param rating the new glicko 2 rating
	 */
	public void setGlicko2Rating(Double rating) {
		this.rating = RatingEngine.convertRatingToOriginalGlickoScale(rating);
	}

	/**
	 * Gets the volatility.
	 *
	 * @return the volatility
	 */
	public Double getVolatility() {
		return volatility;
	}

	/**
	 * Sets the volatility.
	 *
	 * @param volatility the new volatility
	 */
	public void setVolatility(Double volatility) {
		this.volatility = volatility;
	}

	/**
	 * Gets the rating deviation.
	 *
	 * @return the rating deviation
	 */
	public Double getRatingDeviation() {
		return ratingDeviation;
	}

	/**
	 * Sets the rating deviation.
	 *
	 * @param ratingDeviation the new rating deviation
	 */
	public void setRatingDeviation(Double ratingDeviation) {
		this.ratingDeviation = ratingDeviation;
	}

	/**
	 * Return the rating deviation of the player scaled down
	 * to the scale used by the algorithm's internal workings.
	 * 
	 * @return Double
	 */
	public Double getGlicko2RatingDeviation() {
		return RatingEngine.convertRatingDeviationToGlicko2Scale( ratingDeviation );
	}

	/**
	 * Set the rating deviation, taking in a value in Glicko2 scale.
	 *
	 * @param ratingDeviation the new glicko 2 rating deviation
	 */
	public void setGlicko2RatingDeviation(Double ratingDeviation) {
		this.ratingDeviation = RatingEngine.convertRatingDeviationToOriginalGlickoScale( ratingDeviation );
	}

	/**
	 * Used by the calculation engine, to move interim calculations into their "proper" places.
	 * 
	 */
	public void finaliseRating() {
		this.setGlicko2Rating(workingRating);
		this.setGlicko2RatingDeviation(workingRatingDeviation);
		this.setVolatility(workingVolatility);
		
		this.setWorkingRatingDeviation(0.0);
		this.setWorkingRating(0.0);
		this.setWorkingVolatility(0.0);
	}
	
	
	/**
	 * Returns a formatted rating for inspection.
	 *
	 * @return the string
	 */
	@Override
	public String toString() {
		return "Player [firstName=" + firstName + ", lastName=" + lastName + ", rating=" + rating + ", ratingDeviation="
				+ ratingDeviation + ", volatility=" + volatility + ", numberOfResults=" + numberOfResults + "]";
	}
	
	
	/**
	 * Gets the number of results.
	 *
	 * @return the number of results
	 */
	public int getNumberOfResults() {
		return numberOfResults;
	}

	/**
	 * Increment number of results.
	 *
	 * @param increment the number or results by which to increment
	 */
	public void incrementNumberOfResults(int increment) {
		this.numberOfResults = numberOfResults + increment;
	}

	/**
	 * Gets the id.
	 *
	 * @return the id
	 */
	public Long getid() {
		return id;
	}

	/**
	 * Sets the working volatility.
	 *
	 * @param workingVolatility the new working volatility
	 */
	public void setWorkingVolatility(Double workingVolatility) {
		this.workingVolatility = workingVolatility;
	}

	/**
	 * Sets the working rating.
	 *
	 * @param workingRating the new working rating
	 */
	public void setWorkingRating(Double workingRating) {
		this.workingRating = workingRating;
	}

	/**
	 * Sets the working rating deviation.
	 *
	 * @param workingRatingDeviation the new working rating deviation
	 */
	public void setWorkingRatingDeviation(Double workingRatingDeviation) {
		this.workingRatingDeviation = workingRatingDeviation;
	}
}
