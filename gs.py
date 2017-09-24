import sys
if __name__ == "__main__":
   
   # read in input file
   import json
   file_obj = open(sys.argv[1], "r")
   data = file_obj.read()
   decoded = json.loads(data)
   #pref_dict_men = decoded[0][0]
   #pref_dict_women = decoded[0][1]
   #print (pref_dict_men)
   #print (pref_dict_women)
   #inverse = getattr(stable_matching_helpers, inverse_dict)

   # start timer
   import time
   start_time = time.process_time()
   
   # run Gale-Shapley calculations
   #rx = range(0, len(decoded))
   #rx = rx[-1::2]
   #print (len(decoded))
   result = []
   R = {}
   for x in range(0, len(decoded), 1):
      #ry = range(0, len(decoded[x]))
      #ry = ry[-1::2]
      #print (len(decoded[x]))

      #If R has something, put it in the results list
      if len(R) != 0:
         result.append(R);
         R = {}

      for y in range(0, len(decoded[x])-1, 2):
         #print (x)
         #print (y)
         
         #First set of preference data
         pref_dict_men = decoded[x][y]
         #second set of preference data
         pref_dict_women = decoded[x][y+1]
         #print (pref_dict_men)
         #print (pref_dict_women)

         #first set of only keys
         men = list(pref_dict_men.keys())
         #second set of only keys
         women = list(pref_dict_women.keys())
         #print (men)
         #print (women)
         rank_of_men = {}
         i = 1
         #ranking the men in the women's preference lists
         for w in women:
            rank_of_men[w] = {}
            i = 1
            for m in pref_dict_women[w]:
               rank_of_men[w][m] = i
               i += 1

         #creating a place to hold what preference number we are on for each man
         pref_ptr = {}
         for m in men:
            pref_ptr[m] = 0

         S = {}
         total_men = len(men)

         #while there is an unpaired man
         while men:
            #remove an unpaired man
            m = men.pop()
            #if the pointer is greater than the amount of possible pairs, skip
            if pref_ptr[m] > total_men: continue
            #current women based on current man and number on man's preference list
            w = pref_dict_men[m][pref_ptr[m]]
            #increment man's preference list
            pref_ptr[m] += 1
            #if she isn't paired, pair with him
            if w not in S: S[w] = m
            #otherwise check if m is higher on her preference list than her current boo
            else:
               old_boy = S[w]
               #m is better, she takes m and old_boy returns to try to find a new girl
               if rank_of_men[w][m] < rank_of_men[w][old_boy]:
                  S[w] = m
                  men.append(old_boy)
               #if she doesn't like him better, he returns to try to find a new girl
               else:
                  men.append(m)
      #add new pairs to the current dictionary
      R.update([(v, k) for k, v in S.items()])   
      sorted(R)

   #if the dictionary isn't empty, add it to the results list
   if len(R) != 0:
      result.append(R);
      R = {}

   # end timer
   end_time = time.process_time()
   
   # invert S
   #result = dict([(v, k) for k, v in R.items()])
   #print (result)

   # write output file
   file_out = open(sys.argv[2], "w")
   json.dump(result, file_out)
   file_out.close()
   
   # print run time
   print("Ran in: {:.5f} secs".format(end_time - start_time))
   #print (end_time - start_time)
