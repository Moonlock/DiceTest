function histogram(red, yellow, combined, plotTitle, names=[], groups=false)

  if(rows(red) == 1)
    yMax = max([red yellow]);
  else
    yMax = max([sum(red) sum(yellow)]);
  end
  yMax = max(yMax, 1);
  
  if(groups)
    type = "hist";
  else
    type = "stacked";
  end 
  fontSize = 30;

  graphics_toolkit ("fltk");
  
  figure(1);
  set(gcf,'NumberTitle','off');
  set(gcf, 'Name', plotTitle);
  
  subplot(2, 2, 1);

  if(rows(names) == 1 || groups)
    bar(red', type);
  else
    bar(red', type, "facecolor", "red");
  end
  set(gca, "fontsize", fontSize)
  axis([-Inf Inf 0 yMax]);
  xlabel("Red Die");
  ylabel("Frequency");
  
  subplot(2, 2, 2);

  if(rows(names) == 1 || groups)
    bar(yellow', type);
  else
    bar(yellow', type, "facecolor", "yellow");
  end
  set(gca, "fontsize", fontSize)
  axis([-Inf Inf 0 yMax]);
  xlabel("Yellow Die");
  ylabel("Frequency");
  
  subplot(2, 2, [3 4]);
  bar([2 3 4 5 6 7 8 9 10 11 12], combined', type);
  set(gca, "fontsize", fontSize)
  xlabel("Combined Dice");
  ylabel("Frequency");
  legend(names', "location", 'northoutside', 'orientation', 'horizontal');
  
endfunction


