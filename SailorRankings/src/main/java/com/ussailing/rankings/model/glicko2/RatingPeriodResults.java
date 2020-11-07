/*
 * Copyright (C) 2013 Jeremy Gooch <http://www.linkedin.com/in/jeremygooch/>
 *
 * The licence covering the contents of this file is described in the file LICENCE.txt,
 * which should have been included as part of the distribution containing this file.
 */
package com.ussailing.rankings.model.glicko2;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * This class holds the results accumulated over a rating period.
 * 
 * @author Jeremy Gooch
 */
public class RatingPeriodResults {
	private List<Result> results = new ArrayList<>();
	private Set<Player> participants = new HashSet<>();

	
	/**
	 * Create an empty results List.
	 */
	public RatingPeriodResults() {}
	

	/**
	 * Constructor that allows you to initialize the list of participants.
	 * 
	 * @param participants (Set of Player objects)
	 */
	public RatingPeriodResults(Set<Player> participants) {
		this.participants = participants;
	}
	
	
	/**
	 * Add a result to the set.
	 * 
	 * @param winner
	 * @param loser
	 */
	public void addResult(Player winner, Player loser) {
		Result result = new Result(winner, loser);
		
		results.add(result);
	}
	
	
	/**
	 * Record a draw between two players and add to the set.
	 * 
	 * @param player1
	 * @param player2
	 */
	public void addDraw(Player player1, Player player2) {
		Result result = new Result(player1, player2, true);
		
		results.add(result);
	}
	
	
	/**
	 * Get a list of the results for a given player.
	 * 
	 * @param player
	 * @return List of results
	 */
	public List<Result> getResults(Player player) {
		List<Result> filteredResults = new ArrayList<Result>();
		
		for ( Result result : results ) {
			if ( result.participated(player) ) {
				filteredResults.add(result);
			}
		}
		
		return filteredResults;
	}

	
	/**
	 * Get all the participants whose results are being tracked.
	 * 
	 * @return set of all participants covered by the results List.
	 */
	public Set<Player> getParticipants() {
		// Run through the results and make sure all players have been pushed into the participants set.
		for ( Result result : results ) {
			participants.add(result.getWinner());
			participants.add(result.getLoser());
		}

		return participants;
	}
	
	
	/**
	 * Add a participant to the rating period, e.g. so that their rating will
	 * still be calculated even if they don't actually compete.
	 *
	 * @param rating
	 */
	public void addParticipants(Player rating) {
		participants.add(rating);
	}
	
	
	/**
	 * Clear the results Set.
	 */
	public void clear() {
		results.clear();
	}
}
