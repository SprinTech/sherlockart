from database.user_db import user_db_create_table as uc
from database.art_db import art_db_create_table as ac

# create db and tables.
uc.user_db_init()
ac.art_db_init()

# fill the data
uc.user_load_data("./csv/admin_data.csv")
# uc.comment_load_data("./csv/comment_data.csv")
ac.current_load_data("./csv/current_data.csv")
ac.artwork_load_data("./csv/artwork_data.csv")
