import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt


alt.data_transformers.enable("vegafusion")
alt.renderers.enable('jupyterlab')
alt.renderers.enable('mimetype')



def vis_bar(data, x_input, width, height):
    return alt.Chart(data).mark_bar().encode(
        x = x_input,
        y = "count()"
    ).properties(
        width = width, 
        height = height
    )


def var_distribution_plot(data, save_file_path):
    over = vis_bar(data, "over", 150, 150)
    wides = vis_bar(data, "wides", 150, 150)
    noballs = vis_bar(data, "noballs", 150, 150)
    legbyes = vis_bar(data, "legbyes", 150, 150)
    byes = vis_bar(data, "byes", 150, 150)
    wicket = vis_bar(data, "wicket", 150, 150)
    run_batter = vis_bar(data, "runs_batter", 150, 150)
    run_extras = vis_bar(data, "runs_extras", 150, 150)
    run_total = vis_bar(data, "runs_total", 150, 150)
    over_ball = vis_bar(data, "over_ball", 150, 150)
    runs_cumulative = vis_bar(data, "runs_cumulative", 150, 150)

    title_1_a = alt.Chart(
        {"values": [{"text": "Figure 1.1: Distribution of Variables"}]}
    ).mark_text(size=20).encode(
        text="text:N"
    )
    v1 = alt.hconcat(over, wides, noballs)
    v2 = alt.hconcat(legbyes, byes, wicket)
    v3 = alt.hconcat(run_batter, run_extras, run_total)
    v4 = alt.hconcat(over_ball, runs_cumulative)
    chart = alt.vconcat(v1, v2, v3, v4)
    chart.save(save_file_path)
    return chart

def var_distribution_plot2 (data, save_file_path):
    season = vis_bar(data, "season", 500, 150)
    team = vis_bar(data,"team", 900, 150)
    inning = vis_bar(data,"inning:N", 150, 150)
    powerplay = vis_bar(data,"powerplay:N", 150, 150)

    title_1_b = alt.Chart(
        {"values": [{"text": "Figure 1.2: Distribution of Variables"}]}
    ).mark_text(size=20).encode(
        text="text:N"
    )

    h_1 = alt.hconcat(inning, powerplay)
    chart = alt.vconcat(season, team, h_1)
    chart.save(save_file_path)
    return chart

def get_correlation_table(data):
    corr_data = data[["over", "wides", "noballs", "legbyes", "byes", "runs_batter", "runs_extras", "runs_total", "over_ball", "runs_cumulative", "wicket"]]
    corr_df = corr_data.corr()
    corr_df.style.set_caption("Table 4: Correlation Analysis").set_table_styles([{
        'selector': 'caption',
        'props': 'caption-side: bottom; font-size:1.25em;'
    }], overwrite=False)
    return corr_df

def get_correlation_heatmap(data, save_file_path):
    corr_df = get_correlation_table(data)
    corr_ = corr_df.stack()
    corr_ = corr_.reset_index()
    corr_.columns = ['row', 'column', 'corr']

    chart = alt.Chart(corr_).mark_rect().encode(
        x = 'column',
        y = 'row',
        color = 'corr:Q',
        tooltip = 'corr:Q'
    ).properties(
        width = 400,
        height = 400,
        #title = "Figure 2: Correlation Matrix"
    )
    chart.save(save_file_path)
    print(f"Chart saved to: {save_file_path}")

def wicket_by_over_barchart(data, save_file_path):
    over_count_wicket = data.groupby('over')['wicket'].count()
    chart = over_count_wicket.plot(kind = 'bar', xlabel="Over", ylabel="Wicket Count")
                                                    #,title = "Figure 3.1 : Wicket count across overs")
    fig = chart.get_figure()
    fig.savefig(save_file_path)
    print(f"Chart saved to: {save_file_path}")

def wicket_per_over_bar(data, save_file_path):
    inning_count_wicket =  data.groupby('inning')['wicket'].count()
    chart = inning_count_wicket.plot(kind = 'bar', xlabel ='inning', ylabel = 'Wicket Count')
    fig = chart.get_figure()
    fig.savefig(save_file_path)
    print(f"Chart saved to: {save_file_path}")


def wicket_density_histogram(data, save_file_path):
    data_0 = data[data['wicket'] == 0]
    data_1 = data[data['wicket'] == 1]

    plt.hist(data_0['runs_cumulative'],  
            label="Not a Wicket",
            alpha = 0.5, 
            density = True) 
    
    plt.hist(data_1['runs_cumulative'],  
            label="Wicket",
            alpha = 0.5,
            density=True) 
    
    plt.legend(loc='upper right') 
    plt.xlabel("Runs scored until Current Ball in Current Innings")
    plt.ylabel("Probability Density")
    plt.savefig(save_file_path, bbox_inches='tight')
    print(f"Chart saved to: {save_file_path}")

