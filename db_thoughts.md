# Database Design

## Database: SQLite3 for portability

## Table: Photos

1. Photo ID
2. Filepath
3. Date / Time
4. Location
5. File Size
6. ResX
7. ResY
8. Crypographic Hash
9. Image Comparison Hash
10. NextSimilarImage

-> Also add EXIF data potentially, or retrieve it from the files on demand

## Table: Face Hashes (first build algorithm lol)

1. Person ID
2. Photo ID
3. Face Hash

