
SELECT event_id, packets 
FROM cyberpulse_analytics.fct_security_incidents 
WHERE packets <= 0;
