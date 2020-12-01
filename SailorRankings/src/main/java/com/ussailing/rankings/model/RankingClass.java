package com.ussailing.rankings.model;

import com.ussailing.rankings.model.glicko2.RatingEngine;

public enum RankingClass {
	
	LASER(RatingEngine.DEFAULT_TAU, RatingEngine.DEFAULT_VOLATILITY, true, false),
	COLLEGE(RatingEngine.DEFAULT_TAU, RatingEngine.DEFAULT_VOLATILITY, false, false);
	
	private final Double classTau;
	private final Double classVolatility;
	private final Boolean isOneDesign;
	private final Boolean isKeelboat;
	
	private RankingClass(double classTau, double classVolatility, boolean isOneDesign, boolean isKeelboat) {
		this.classTau = classTau;
		this.classVolatility = classVolatility;
		this.isOneDesign = isOneDesign;
		this.isKeelboat = isKeelboat;
	}

	public synchronized Double getClassTau() {
		return classTau;
	}

	public synchronized Double getClassVolatility() {
		return classVolatility;
	}

	public synchronized Boolean getIsOneDesign() {
		return isOneDesign;
	}

	public synchronized Boolean getIsKeelboat() {
		return isKeelboat;
	}
}
