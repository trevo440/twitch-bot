CREATE TABLE IF NOT EXISTS users (
	UserID text PRIMARY KEY,
	MessagesSent integer Default 0,
	Coins integer Default 0,
	CoinLock text DEFAULT CURRENT_TIMESTAMP 
);