import duckdb

con = duckdb.connect()

con.execute("PRAGMA enable_progress_bar")


df = con.execute(
    """
    SELECT X, Y, Z, sphere_name
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY sphere_name
                   ORDER BY dist_from_cluster ASC
               ) AS dist_rank,
               COUNT(*) OVER (
                   PARTITION BY sphere_name
               ) AS n_in_sphere
        FROM (
            SELECT 
                source_id,
                delta_vT,
                sphere_name,
                X,
                Y,
                Z,
                dist_from_cluster,
                ROW_NUMBER() OVER (
                    PARTITION BY source_id
                    ORDER BY delta_vT ASC
                ) AS rn
            FROM read_parquet('/Volumes/travelpassport/tables/dvt_less_than_5.parquet')
            WHERE delta_vT < 0.5
        )
        WHERE rn = 1
    )
    WHERE dist_rank <= 0.1 * n_in_sphere
    """
).df()


# df = con.execute(
#     """
#     SELECT X, Y, Z, sphere_name
#     FROM (
#         SELECT *,
#                ROW_NUMBER() OVER (
#                    PARTITION BY sphere_name
#                    ORDER BY RANDOM()
#                ) AS rand_rank,
#                COUNT(*) OVER (
#                    PARTITION BY sphere_name
#                ) AS n_in_sphere
#         FROM (
#             SELECT
#                 source_id,
#                 delta_vT,
#                 sphere_name,
#                 X,
#                 Y,
#                 Z,
#                 ROW_NUMBER() OVER (
#                     PARTITION BY source_id
#                     ORDER BY delta_vT ASC
#                 ) AS rn
#             FROM read_parquet('/Volumes/travelpassport/tables/dvt_less_than_5.parquet')
#             WHERE delta_vT < .2
#         )
#         WHERE rn = 1
#     )
#     WHERE rand_rank <= 0.5 * n_in_sphere
#     """
# ).df()

# df = con.execute(
#     """
#     SELECT X, Y, Z, sphere_name
#     FROM (
#         SELECT
#             source_id,
#             delta_vT,
#             sphere_name,
#             X,
#             Y,
#             Z,
#             ROW_NUMBER() OVER (
#                 PARTITION BY source_id
#                 ORDER BY delta_vT ASC
#             ) AS rn
#         FROM read_parquet('/Volumes/travelpassport/tables/dvt_less_than_5.parquet')
#         WHERE delta_vT < 1
#     )
#     WHERE rn = 1
#     """
# ).df()


df.to_csv("/Volumes/travelpassport/tables/candidates_ThreeWidget.csv", index=False)

# con = duckdb.connect()

# foo = con.execute("""
#     DESCRIBE SELECT *
#     FROM read_parquet('/Volumes/travelpassport/tables/dvt_less_than_5.parquet')
# """).fetchdf()
