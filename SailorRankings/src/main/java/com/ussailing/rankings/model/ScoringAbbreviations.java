/*
 * Copyright (c) 2020 as part of SailorRankings, All rights reserved.
 * @author Dan Birmingham. Please reach out to dgbirm@gmail.com
 * Date generated: Nov 30, 2020
 * @version jdk-11
 */
package com.ussailing.rankings.model;

/**
 * The Enum ScoringAbbreviations. Represents the possible non-numeric results a sailor
 * may have for a given race. Different lettered results are handled differently
 * by the rating system. See RRS Appendix A11.
 */
public enum ScoringAbbreviations {

	/** Did not compete. */
	DNC(false),
	
	/** Did not start. */
	DNS(false),
	
	/** On course side. */
	OCS(true),
	
	/** 20-percent scoring penalty. */
	ZFP(true),
	
	/** U-flagged. */
	UFD(true),
	
	/** Black-flagged. */
	BFD(true),
	
	/** Scoring Penalty applied. */
	SCP(true),
	
	/** Did not finish. */
	DNF(false),
	
	/** Retire after finish. */
	RET(false),
	
	/** Disqualified. */
	DSQ(true),
	
	/** Disqualified (non-excludable). */
	DNE(true),

	/** Redress. */
	RDG(true),
	
	/** Discretionary penalty imposed. */
	DPI(true);
	
	private final Boolean isCounted;
	
	
	private ScoringAbbreviations(Boolean isCounted) {
		this.isCounted = isCounted;
	}

	public synchronized Integer calculatedScore(int numberOfParticpants) throws Exception {
		if (!this.isCounted) throw new IllegalCallerException(
				"This Scoring Abbreviation is not counted by the system");
		switch (this) {
		case DNC:
		case DNS:
		case OCS:
		case UFD:
		case BFD:
		case DNF:
			return numberOfParticpants + 1;
		case ZFP:
			return Math.min(
					Math.round((0.2f*(DNF.calculatedScore(numberOfParticpants)))),
					DNF.calculatedScore(numberOfParticpants)
				);

		default:
			throw new Exception("Scoring handled on a case by case basis");
		}
	}

	public synchronized Boolean getIsCounted() {
		return isCounted;
	}
	
}
