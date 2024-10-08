import streamlit as st
import pandas as pd
import os
from in_use import df_fixer, get_balls_data, get_images_list, get_masked_df, load_sam_model, load_image, show_anns
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math
import altair as alt

st.set_page_config(layout="wide")

st.markdown('# Rock fragmentation analysis')
st.markdown('## semi-Decorous edition')


mask_generator= load_sam_model('vit_b')


col_image_selector, col_diameter_imput, col_units = st.columns(3)

with col_image_selector:
    image_selected = st.selectbox('Images: ', options=get_images_list(), index=0)

with col_diameter_imput:
    diameter = st.number_input("Insert Ball's diameter", min_value=1.0, value=10.0, step=1.0)

with col_units:
    units = st.selectbox('Units: ', options=['cm', 'in'], index=0)

original_image, resized_image = load_image(image_selected)
# st.image(image, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
# st.image(original_image, caption='Original Image', width=200,  use_column_width=50, clamp=False, channels="RGB", output_format="auto")

area_ball = math.pi*diameter*diameter/4.0

masks = mask_generator.generate(resized_image)
df_masks = get_masked_df(masks)
beta_df_balls = get_balls_data(resized_image)

df_balls_data = df_fixer(beta_df_balls, diameter, beta_df_balls)
df_masks = df_fixer(df_masks, diameter, beta_df_balls)

# with col_balls_data:
#     st.write('Balls data')
#     st.write(df_balls_data)


# st.write('Masks Dataframe')
# st.write(df_masks)

# st.write('')
# st.write('Masks Stadistics')
# st.write(df_masks.describe())

plot_fig = show_anns(masks,resized_image, df_masks['area_pixel'].quantile(0.8))
# st.image(plot_fig, caption='Masked Image')

# fig, ax = plt.subplots()
# df_masks['area'].hist(bins=100,ax=ax)
# # x=df_masks['area'].quantile(0.8)
# ax.axvline(x=df_masks['area'].quantile(0.8), c='r', label='P80')
# ax.set_ylabel(f'Area {units}^2')
# ax.set_xlabel('Number of Fragments')
# plt.legend()

# plt.title('Area Histogram, P80: ' + str(round(df_masks['area'].quantile(0.8),1)) + f'{units}^2')
# st.pyplot(fig)
# # st.bar_chart(data=x, *, x=None, y=None, x_label='Number of Fragments', y_label=f'Area {units}^2')

# fig, ax = plt.subplots()
# df_masks['diameter'].hist(bins=100,ax=ax)
# ax.axvline(x=df_masks['diameter'].quantile(0.8), c='r', label='P80')
# ax.set_ylabel(f'Diameter {units}')
# ax.set_xlabel('Number of Fragments')
# plt.legend()

# plt.title('Diameter Histogram, P80: ' + str(round(df_masks['diameter'].quantile(0.8),1)) + f'{units}')
# st.pyplot(fig)

# All outputs
col1, col2 = st.columns(2)
with col1:
  st.expander('Orignal Image')
  st.image(original_image, caption="Orignal Image",width=500,  use_column_width=100, clamp=False, channels="RGB", output_format="auto")
with col2:
  # plot_fig = show_anns(masks,resized_image, df_masks['area_pixel'].quantile(0.8))
  st.image(plot_fig, caption='Masked Image',width=500,  use_column_width=100, clamp=False, channels="RGB", output_format="auto")
# csv data
exp1, exp2 = st.columns(2)
with exp1:
    st.write('Masks Dataframe')
    st.write(df_masks)
# Describe
with exp2:
    st.write('')
    st.write('Masks Stadistics')
    st.write(df_masks.describe())

p80 = df_masks['area'].quantile(0.8)
# graph1 
grp1, grp2 = st.columns(2)
with grp1:
#     fig, ax = plt.subplots()
#     df_masks['area'].hist(bins=100,ax=ax)
# # x=df_masks['area'].quantile(0.8)
#     ax.axvline(x=df_masks['area'].quantile(0.8), c='r', label='P80')
#     ax.set_ylabel(f'Area {units}^2')
#     ax.set_xlabel('Number of Fragments')
#     plt.legend()

# # gaph2 
#     plt.title('Area Histogram, P80: ' + str(round(df_masks['area'].quantile(0.8),1)) + f'{units}^2')
#     st.pyplot(fig)
# st.bar_chart(data=x, *, x=None, y=None, x_label='Number of Fragments', y_label=f'Area {units}^2')
    

# Create a histogram chart using Altair
    chart = alt.Chart(df_masks).mark_bar().encode(
        alt.X('area:Q', bin=alt.Bin(maxbins=100), title=f'Area {units}^2'),
        alt.Y('count()', title='Number of Fragments')
      ).properties(
          title=f'Area Histogram, P80: {round(p80, 1)} {units}^2'
      ).interactive()

# Add P80 line
    p80_line = alt.Chart(pd.DataFrame({'P80': [p80]})).mark_rule(color='red').encode(
    x='P80:Q'
    )

# Combine the histogram and P80 line
    final_chart = chart + p80_line

# Display the chart using Streamlit
    st.altair_chart(final_chart, use_container_width=True) 

with grp2:
    # fig, ax = plt.subplots()
    # df_masks['diameter'].hist(bins=100,ax=ax)
    # ax.axvline(x=df_masks['diameter'].quantile(0.8), c='r', label='P80')
    # ax.set_ylabel(f'Diameter {units}')
    # ax.set_xlabel('Number of Fragments')
    # plt.legend()

    # plt.title('Diameter Histogram, P80: ' + str(round(df_masks['diameter'].quantile(0.8),1)) + f'{units}')
    # st.pyplot(fig)
    units = str(units)
    # p80 = df_masks['area'].quantile(0.8)
    diameter_chart = alt.Chart(df_masks).mark_bar().encode(
    alt.X('diameter:Q', bin=alt.Bin(maxbins=100), title=f'Diameter {units}'),
    alt.Y('count()', title='Number of Fragments')
    ).properties(
      title=f'Diameter Histogram, P80: {round(diameter, 1)} {units}'
    ).interactive()

# Add P80 line
    p80_diameter_line = alt.Chart(pd.DataFrame({'P80': [diameter]})).mark_rule(color='red').encode(
        x='P80:Q'
    )

# Combine the histogram and P80 line
    final_diameter_chart = diameter_chart + p80_diameter_line

# Display the chart using Streamlit
    st.altair_chart(final_diameter_chart, use_container_width=True)
