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
   
%  graphics_toolkit ("fltk");
  figure(1);
  set(gcf,'NumberTitle','off');
  set(gcf, 'Name', plotTitle);
  
  subplot(2, 2, 1);
  bar(red', type);
  axis([-Inf Inf 0 yMax]);
  xlabel("Red Die");
  ylabel("Frequency");
  
  subplot(2, 2, 2);
  bar(yellow', type);
  axis([-Inf Inf 0 yMax]);
  xlabel("Yellow Die");
  ylabel("Frequency");
  
  subplot(2, 2, [3 4]);
  bar([2 3 4 5 6 7 8 9 10 11 12], combined', type);
  xlabel("Combined Dice");
  ylabel("Frequency");
  legend(names', "location", 'northoutside', 'orientation', 'horizontal');
  
endfunction