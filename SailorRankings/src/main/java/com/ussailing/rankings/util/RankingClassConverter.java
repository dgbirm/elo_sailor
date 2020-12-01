package com.ussailing.rankings.util;

import java.util.stream.Stream;

import javax.persistence.AttributeConverter;
import javax.persistence.Converter;
import javax.persistence.PersistenceException;

import com.ussailing.rankings.model.RankingClass;

@Converter(autoApply = true)
public class RankingClassConverter implements AttributeConverter<RankingClass, String> {

	@Override
	public String convertToDatabaseColumn(RankingClass rankingClass) {
		if (rankingClass == null) throw new PersistenceException(
				"Ranked Sailors must have a class");
		return rankingClass.name();
	}

	@Override
	public RankingClass convertToEntityAttribute(final String dbData) {
		if (dbData == null) throw new IllegalArgumentException(
				"Ranked Sailors must have a class");
		return Stream.of(RankingClass.values())
				.filter(rc -> rc.name().equals(dbData))
				.findFirst()
				.orElseThrow(IllegalArgumentException::new);
	}
	
}
