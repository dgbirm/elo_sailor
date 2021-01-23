package com.ussailing.rankings.model;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.Table;

import com.ussailing.rankings.model.glicko2.Player;
 
@Entity
@Table(name = "Sailor")
public class Sailor extends Player implements ISailorModel{
	
	private static final long serialVersionUID = -9070223475888842325L; //default generated
	
	@Enumerated(EnumType.STRING)
	@Column(name = "rankingClass", updatable = false, nullable = false)
	private RankingClass rankingClass;

	public Sailor(String firstName, String lastName, RankingClass rankingClass) {
		super(firstName, lastName);
		this.rankingClass = rankingClass;
		
	}
	
	public Sailor(String firstName, String lastName, Double initRating, Double initRatingDeviation,
			Double initVolatility, RankingClass rankingClass) {
		super(firstName, lastName, initRating, initRatingDeviation, initVolatility);
		this.rankingClass = rankingClass;
	}
	
	public Sailor() {
		super();
	}
	
	

}
