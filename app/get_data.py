import asyncio
from wrs import ConvertToWRS
from catalog import get_items, get_image
from odc import add_item
from pathlib import Path


async def main():
    print("Loading WRS...", end='')
    wrs = ConvertToWRS()
    print("OK")

    lon1, lon2 = 131.5, 132.5
    lat1, lat2 = 42.5, 43.5
    limit = 1
    days = 30
    dates = ('2021-06-01', '2021-07-30')

    wrs_list = wrs.get_wrs_list(lon1, lat1, lon2, lat2)
    items = await get_items(wrs_list, dates=dates, limit=limit, days=days)
    for item in items["items"]:
        print(item)
    
    names = [f'B{i}' for i in range(1, 12) ] + ['BQA']
    path = Path() / 'data' / items['items'][0]['assets']['B1']['href'].split("/")[-2]
    if not path.exists():
        path.mkdir()
    urls = [items['items'][0]['assets'][name]['href'] for name in names]
    tasks = [get_image(url, path) for url in urls]
    await asyncio.gather(*tasks)    
    return items


if __name__ == "__main__":
    result = asyncio.run(main())
   # print(result)