SELECT
    COUNT(*),
    AVG(c.households_median_income_dollars)
FROM
    userstats AS u
LEFT OUTER JOIN pluto AS p ON u.bbl = p.bbl
LEFT OUTER JOIN census AS c ON
    p.borocode = c.borocode AND p.tract2010 = c.tract2010
WHERE
    length(u.bbl) > 0
    AND u.letter_mail_choice = 'WE_WILL_MAIL'
