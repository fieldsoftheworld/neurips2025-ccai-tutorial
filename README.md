# FTW Tutorial
Tutorial submission for the Climate Change AI workshop at NeurIPS 2025

## Tutorial outline
### Overview/objectives
- Use the Fields of The World benchmark and CLI to support agricultural analyses relevant to climate change and biodiversity
- Create a new field boundary dataset that can be used for downstream tasks
  - Crop type classification
  - Change detection ?
  - Yield if we're feeling really ambitious / find a nice field level yield dataset (theoretically exists)
  - Cross with land cover map over multiple years to "detect" deforestation within boundaries using GLAD deforestation map or MapBiomas? (EUDR use case)

### Climate impact
In this section, describe in more detail how the methods or tools introduced in this tutorial could have pathways to positive impact regarding climate change. The problem should be clearly explained and motivated for non-experts. Feel free to discuss relevant research works, real-world examples of successful applications, and/or climate startups or organizations that are making an impact using similar methods or tools to address climate-related challenges.

We also ask that authors emphasize the real-world impact of the methods, specifically: Who will be using the models? How will the models be used? What decisions will be made based on the outputs of these models? How will they impact existing systems/the environment/communities on the ground?

### Target audience
- Agronomists?
- Remote sensing people?
- Machine learning practitioners for agriculture use cases?
- Supply chain people?
- Should we tell the story as one of these people? e.g. "Suppose you are a \__ wanting to\__..."

### Outline
1. Choose an ROI and TOI
    - [bbox finder](https://bboxfinder.com/#0.000000,0.000000,0.000000,0.000000)?
    - admin1 or admin2 dropdown?
    - the ROI needs to be <1 Sentinel-2 tile - select an MGRS tile?

2. Download Sentinel-2 images for window A and window B (using crop calendar-based auto selection)
   
4. Predict field boundaries
    - `ftw inference run`
  
4. Post-process field boundaries
    - filter by land cover map (`ftw inference filter_by_lulc`)
    - polygonize and smooth/filter by size (`ftw inference polygonize`)

5. Zonal stats
  
6. Create embeddings for fields
    - AlphaEarth Foundations (from HuggingFace catalog? or ask Cholmes to do it for our  area?)
    - MOSAIKS (have to choose time range)
    - Presto (have to choose time range)
  
7. Crop type classification of field boundaries (USA)
    - Caleb's demo and/or Hannah's notebook
    - would be nice if we had an example for another country than the US
  
8. Deforestation mapping (Brazil or somewhere in Latin America?)
    - pair with GLAD deforestation map
    - Hannah will send example area with deforestation
  
9. Change detection
    - visualize changes in embeddings?
  
10. Clustering?? what else can we get "for free"

### Tell us how you used this tutorial
Some sort of google form or message board where we can track the use cases people are doing with it + benefits of having made it?

## Formatting/guidelines
- [NeurIPS Tutorial Template](https://colab.research.google.com/drive/16OJ1ihddpC5rwUaAv7KZnRO7L0miypE5?usp=sharing)
- [CCAI Tutorial Guidelines](https://docs.google.com/document/d/1Yb_L_yasBnzxuRPHe3FiGaChk3BgQ8UVSHGt-75F_OA/edit?tab=t.0)

## Tutorial fodder
- Gedeon’s inference notebook [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1nQdUWEmX79XjWiPTUCUoYUNH3fsQjwmu?usp=sharing)
- Nathan’s stuff from in person sprint
    - Trying to understand issues with AWS and Planetary Computer imagery: https://colab.research.google.com/drive/1mp3B0_UCkL5YzPVZl1Qti065ozICbnmN
    - An end-to-end inference demo: https://colab.research.google.com/drive/1jxTqcUmq-UO-NioZTZ43JBCb0UOk7gPR#scrollTo=23374c2d-0b01-496c-8171-3abf13dc77d4
    - Another inference demo, not sure how it’s different from the last one: https://colab.research.google.com/drive/1jE9hp99GAqzUkqj2Mdci27z61b6Ffidp#scrollTo=X0S7WNEbMeJR
- Ivan: wrote a colab notebook a while ago for getting and visualizing boundaries using Microsoft Planetary computer and CLI: https://colab.research.google.com/drive/1s20w-PzuYQvIfeZyMCiB3qRjO0w_5K1l?usp=sharing
- Caleb tutorial on [crop type classification using CDL](https://colab.research.google.com/drive/1H8_kiWEJlehPni34sULK-3LsMjOvpCT4?usp=sharing)
- Hannah notebook for [pre-season crop type classification using CDL](https://colab.research.google.com/drive/1xocIpw2FGYhkk4B3fgy7vA-McdszkcfP?usp=sharing)
