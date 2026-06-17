# connect to db
from astrapy import DataAPIClient
from dotenv import load_dotenv
import os
# create collections
from astrapy.info import (
    CreateTableDefinition,
    ColumnType,
    AlterTableAddColumns,
    ColumnType,
    TableScalarColumnTypeDescriptor,
)
from astrapy.constants import VectorMetric

load_dotenv()

def connectDB():
    client = DataAPIClient()
    db = client.get_database(
        api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
        token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
    )
    print(f"Connected to Astra DB: {db.list_collection_names()}")
    return db

# create collection
# collection = DB_INSTANCE.create_collection(
#     "job_scraper"
# )

# print(f"Collection 'job_scraper' created successfully!")

# # create table
def create_table(DB_INSTANCE):
  table = DB_INSTANCE.create_table(
      "reels_id",
      definition=(
          CreateTableDefinition.builder()
          .add_column("id", ColumnType.TEXT)
          .add_column("title", ColumnType.TEXT)
          .add_column("description", ColumnType.TEXT)
          .add_column("channel", ColumnType.TEXT)
          .add_column("uploader", ColumnType.TEXT)
          .add_column("uploader_id", ColumnType.TEXT)
          .add_column("like_count", ColumnType.INT)
          .add_column("comment_count", ColumnType.INT)
          .add_column("duration", ColumnType.DOUBLE)
          .add_column("uploaded_at", ColumnType.TIMESTAMP)
          .add_column("downloaded", ColumnType.BOOLEAN)
          .add_column("processed", ColumnType.BOOLEAN)
          .add_column("video_path", ColumnType.TEXT)
          .add_column("ocr_text", ColumnType.TEXT)
          .add_column("ocr_processed", ColumnType.BOOLEAN)
          .add_column("transcript", ColumnType.TEXT)
          .add_column("transcript_processed", ColumnType.BOOLEAN)
          .add_column("final_job_data", ColumnType.TEXT)
          .add_partition_by("id")
          .build()
      ),
  )
  print(f"Table 'reels_id' created successfully!")

# create_table()


# table = DB_INSTANCE.get_table("reels_id")

# Add columns to the existing table
# def alter_table():
#   table.alter(
#       AlterTableAddColumns(
#           columns={
#               "final_job_data": TableScalarColumnTypeDescriptor(
#                   column_type=ColumnType.TEXT,
#               ),
#           },
#       ),
#   )
#   print(f"Table 'reels_id' altered successfully!")

# alter_table()


# def drop_table():
#     DB_INSTANCE.drop_table("reels_id")
#     print(f"Table 'reels_id' dropped successfully!")

# drop_table()