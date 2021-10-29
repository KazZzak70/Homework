## Pure Python command-line RSS reader.
This folder will contain JSON-files with data parsed from resources
## JSON-file structure:
```
{
    "feed": resource name,
    "items": [
        {
            "title": news title,
            "description": news description,
            "link": link to news,
            "pubdate": news publication date,
            "links": {
                "1": link to news,
                "2": link to some media
            }
        },
        ...
        ]
}
```