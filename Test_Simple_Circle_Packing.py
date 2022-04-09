import matplotlib.pyplot as plt
import pandas as pd
import circlify

df = pd.DataFrame({
    'Name': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
    'Value': [400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400, 400]})

# compute circle positions:
circles = circlify.circlify(
    df['Value'].tolist(),
    show_enclosure=True,
    target_enclosure=circlify.Circle(x=0, y=0, r=1680))

fig, ax = plt.subplots(figsize=(10,10))

lim = max(
    max(
        abs(circle.x) + circle.r,
        abs(circle.y) + circle.r,
    )
    for circle in circles
)
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)

print (circles)
for circle in circles:
    x, y, r = circle
    ax.add_patch(plt.Circle((x, y), r, alpha=0.2, linewidth=2, fill=False))

plt.show()