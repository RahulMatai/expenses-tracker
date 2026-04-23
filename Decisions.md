# All about decisions and precisions


## 1. Money Handling

**Decision:** Store amounts as integer paise (₹ × 100) in SQLite. Use Python `Decimal` for all calculations — never `float`.

**Why:**
- `float` has binary precision issues e.g. `0.1 + 0.2 = 0.30000000000000004`
- Storing as paise (integer) means zero decimal math in the DB
- `Decimal` gives exact arithmetic when converting back to ₹ for display

**Trade-off:** Slightly more conversion code but 100% correct money handling.

## 2 choosing SQLlite over PostgreSQL

**Decision:** SQLite was chosen for simplicity, but we can migrate it to PostgreSQL

**why** 
- sqloite is built in no hassle for third setup, fast for personal tracking,acceptable for the time bound project.

**tradeoff:** Lacks production qualtiyu on streamlit Cloud, in actual Envoirment we would use PostgreSQL.


## 3. idempoyency

**Decision:** Each submission carries unique client ID (UUID).

**why** 
- User might click submit twice low bandwidth issue sometimes takes time to refresh, Unique contraint on 'client_id' silently ignores dubplicate.

**tradeoff:** More Session stage management for UI



## 4. Design Decisions and Trade offs

**what we achieved** 
- SQLite for storage, as built in python
- Paisa (integer) storage for money no float precision bugs
- Decimal for all calulations

**Actul Trade offs** 
- Sqlite resets on streamlit cloud restarts
- no delete or edit expenses features
- single user assumed
- no Pagination for personal use.
