# import pandas as pd

# data=pd.read_json("zee5_show_list_Jun26.json")

# data.to_csv("data.csv",index=False)
# import pandas as pd
# import json

# # Load the JSON data from the file
# with open('/home/link-lap-24/prabhat/zee5_show_list_Jun26.json', 'r') as file:
#     data = json.load(file)

# # Transform the data into a tabular format
# rows = []
# for show, cast in data.items():
#     for member in cast:
#         rows.append({"Show": show, "Cast": member})

# # Create a DataFrame from the rows
# df = pd.DataFrame(rows)

# # Save the DataFrame to a CSV file
# df.to_csv('zee5_show_list.csv', index=False)

import pandas as pd
import json

# Load the JSON data from the file
with open('/home/link-lap-24/prabhat/zee5_show_list_Jun26.json', 'r') as file:
    data = json.load(file)

# Transform the data into a tabular format
rows = []
for show, cast in data.items():
    # Join cast members into a single string
    cast_str = ', '.join(cast)
    rows.append({"Show": show, "Cast": cast_str})

# Create a DataFrame from the rows
df = pd.DataFrame(rows)

# Save the DataFrame to a CSV file
df.to_csv('zee5_show_list2.csv', index=False)

