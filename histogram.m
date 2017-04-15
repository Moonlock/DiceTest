function histogram(red, yellow, combined)

  if(rows(red) == 1)
    yMax = max([red yellow]);
  else
    yMax = max([sum(red) sum(yellow)]);
  end
  
  figure(1);
  
  subplot(2, 2, 1);
  bar(red', "stacked");
  axis([-Inf Inf 0 yMax])
  
  subplot(2, 2, 2);
  bar(yellow', "stacked");
  axis([-Inf Inf 0 yMax])
  
  subplot(2, 2, [3 4]);
  bar([2 3 4 5 6 7 8 9 10 11 12], combined', "stacked");
  
endfunction