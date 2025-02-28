d3.csv('../data/csv/parallel_coordinates_df.csv', function(d){
    return {
      'Model': d['Model'], 
      'Accuracy': +d['Accuracy'],
      'Class 3 Precision': +d['Class 3 Precision'],
      'Class 4 Precision': +d['Class 4 Precision'],
      'Class 3 Recall': +d['Class 3 Recall'],
      'Class 4 Recall': +d['Class 4 Recall']
    };
  }).then(function(dat) {
    
    // Create the plot
    const height = 350;
    const width = 700;
    
    const chart = vl
      .markLine()
      .encode(
        vl.x().fieldN("Model").sort(["Standard XGBoost", "Class Imbalance XGBoost (SMOTE)", "Tuned XGBoost", "Random Forest"]).title("Model"),
        vl.y().fieldQ("Accuracy").title("Accuracy"),
        vl.color().fieldN("Model").scale({ domain: ['Standard XGBoost', 'Class Imbalance XGBoost (SMOTE)', 'Tuned XGBoost', 'Random Forest'], range: ['#ff4500', '#ffa205', '#d40637', '#5f0922'] }),
        vl.opacity().value(0.7)
      )
      .data(dat)
      .width(width)
      .height(height)
      .render();
  });
  