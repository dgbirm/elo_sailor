/*
 * Copyright (C) 2013 Jeremy Gooch <http://www.linkedin.com/in/jeremygooch/>
 *
 * The licence covering the contents of this file is described in the file LICENCE.txt,
 * which should have been included as part of the distribution containing this file.
 */
package com.ussailing.rankings.model.glicko2;

/**
 * Represents the result of a match between two players.
 * 
 * @author Jeremy Gooch
 */
public class Result {
	private static final double POINTS_FOR_WIN = 1.0;
	private static final double POINTS_FOR_LOSS = 0.0;
	private static final double POINTS_FOR_DRAW = 0.5;
	
	private boolean isDraw = false;
	private Player winner;
	private Player loser;
	
	
	/**
	 * Record a new result from a match between two players.
	 * 
	 * @param winner
	 * @param loser
	 */
	public Result(Player winner, Player loser) {
		if (! validPlayers(winner, loser)) 
			throw new IllegalArgumentException();

		this.winner = winner;
		this.loser = loser;
	}
	
	
	/**
	 * Record a draw between two players.
	 * 
	 * @param player1
	 * @param player2
	 * @param isDraw (must be set to "true")
	 */
	public Result(Player player1, Player player2, boolean isDraw) {
		if (! isDraw || ! validPlayers(player1, player2)) 
			throw new IllegalArgumentException();
		
		this.winner = player1;
		this.loser = player2;
		this.isDraw = true;
	}

	
	/**
	 * Check that we're not doing anything silly like recording a match with only one player.
	 * 
	 * @param player1
	 * @param player2
	 * @return
	 */
	private boolean validPlayers(Player player1, Player player2) {
		return !player1.equals(player2);
	}
	
	
	/**
	 * Test whether a particular player participated in the match represented by this result.
	 * 
	 * @param player
	 * @return boolean (true if player participated in the match)
	 */
	public boolean participated(Player player) {
		return (winner.equals(player) || loser.equals(player)); 
	}
	
	
	/**
	 * Returns the "score" for a match.
	 * 
	 * @param player
	 * @return 1 for a win, 0.5 for a draw and 0 for a loss
	 * @throws IllegalArgumentException
	 */
	public double getScore(Player player) throws IllegalArgumentException {
		if ( winner.equals(player) ) return POINTS_FOR_WIN;
		if ( loser.equals(player) ) return POINTS_FOR_LOSS;
		if ( isDraw ) return POINTS_FOR_DRAW;
		throw new IllegalArgumentException("Player " + player.getid() + " did not participate in match");
	}
	
	
	/**
	 * Given a particular player, returns the opponent.
	 * 
	 * @param player
	 * @return opponent
	 */
	public Player getOpponent(Player player) {
		if ( winner.equals(player) ) return loser;
		if ( loser.equals(player) ) return winner;			
		throw new IllegalArgumentException("Player " + player.getid() + " did not participate in match");
	}
	
	
	public Player getWinner() {
		return this.winner;
	}

	
	public Player getLoser() {
		return this.loser;
	}
}
