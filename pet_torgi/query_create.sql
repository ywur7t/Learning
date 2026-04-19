CREATE DATABASE IF NOT EXISTS spimex;
USE spimex;


CREATE TABLE IF NOT EXISTS trades_staging
(
instrument_code String,
instrument_name String,
delivery_basis String,
volume_import_units UInt64,
volume_import_rub UInt64,
changes_to_previous_rub Decimal64(4),
changes_to_previous_pers Decimal64(4),
price_min Decimal64(4),
price_avg Decimal64(4),
price_max Decimal64(4),
price_market Decimal64(4),
price_best_offer Decimal64(4),
price_best_demand Decimal64(4),
count_contracts UInt32,
date Date
)
ENGINE = MergeTree
ORDER BY (date, instrument_code)

insert into trades_staging select * from file('17-04-2026.parquet', Parquet);


select * from trades_staging;


drop tables if exists ___;
-- Daily summary:
select date, SUM(volume_import_rub) as total_volume_rub, SUM(count_contracts) as total_contracts
from trades_staging
group by date
order by date

-- Instrument stats

select instrument_code, sum(volume_import_units) as total_volume, avgWeighted(cast(price_avg, 'UInt32'), count_contracts) as avg_price, sum(count_contracts) as total_contracts
from trades_staging
group by instrument_code
order by total_contracts Desc

-- Price dynamics
select instrument_code, price_avg, date 
from trades_staging
