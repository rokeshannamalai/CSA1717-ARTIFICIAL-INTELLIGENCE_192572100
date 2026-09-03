# Intelligent Business Analytics Platform - Design Task Demo
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("RetailAIDesign").master("local[*]").getOrCreate()
sc = spark.sparkContext

# product, category, quantity, price, stock, customer
data = [
 ("P101","Beverages",12,40.0,18,"C01"),
 ("P101","Beverages",8,40.0,10,"C02"),
 ("P102","Snacks",20,25.0,35,"C01"),
 ("P102","Snacks",15,25.0,20,"C03"),
 ("P103","Grocery",5,120.0,6,"C02"),
 ("P103","Grocery",7,120.0,4,"C04"),
 ("P104","Personal Care",4,180.0,25,"C01"),
 ("P104","Personal Care",6,180.0,19,"C03")
]
rdd=sc.parallelize(data)

sales=rdd.map(lambda x:(x[0],x[2]*x[3])).reduceByKey(lambda a,b:a+b)
qty=rdd.map(lambda x:(x[0],x[2])).reduceByKey(lambda a,b:a+b)

print("\n=== SALES VALUE ===")
for p,v in sales.collect(): print(p, "Rs.", round(v,2))

print("\n=== QUANTITY SOLD ===")
for p,q in qty.collect(): print(p,q)

print("\n=== LOW STOCK ===")
for p,s in rdd.filter(lambda x:x[4]<=6).map(lambda x:(x[0],x[4])).distinct().collect():
    print("RESTOCK:",p,"stock =",s)

print("\n=== TOP PRODUCT RECOMMENDATIONS ===")
for p,q in qty.sortBy(lambda x:x[1],ascending=False).take(3):
    print("Promote/maintain",p,"quantity sold =",q)

print("\n=== CUSTOMER-PRODUCT INTERACTIONS ===")
for (c,p),q in rdd.map(lambda x:((x[5],x[0]),x[2])).reduceByKey(lambda a,b:a+b).collect():
    print(c,p,q)

avg=rdd.map(lambda x:x[2]*x[3]).mean()
print("\n=== ANOMALY CHECK ===")
print("Average transaction value:",round(avg,2))
for x in rdd.filter(lambda x:x[2]*x[3]>2*avg).collect():
    print("Potential anomaly:",x)

print("\n=== SUPPLY CHAIN REORDER ===")
for p,(sold,stock) in rdd.map(lambda x:(x[0],(x[2],x[4]))).reduceByKey(lambda a,b:(a[0]+b[0],min(a[1],b[1]))).filter(lambda x:x[1][1]<=6).collect():
    print(p,"sold =",sold,"minimum stock =",stock)

spark.stop()
