
create (a:StreetCorner {name:"A"})
create (b:StreetCorner {name:"B"})
create (c:StreetCorner {name:"C"})
create (d:StreetCorner {name:"D"})
create (e:StreetCorner {name:"E"})
create (f:StreetCorner {name:"F"})
create (g:StreetCorner {name:"G"})
create (h:StreetCorner {name:"H"})
create (i:StreetCorner {name:"I"})

create (a)-[:Connected {timeToNode:5}]->(b)
create (b)-[:Connected {timeToNode:6}]->(c)
create (b)-[:Connected {timeToNode:3}]->(e)
create (c)-[:Connected {timeToNode:4}]->(i)
create (a)-[:Connected {timeToNode:3}]->(d)
create (d)-[:Connected {timeToNode:4}]->(e)
create (d)-[:Connected {timeToNode:1}]->(b)
create (d)-[:Connected {timeToNode:1}]->(h)
create (e)-[:Connected {timeToNode:5}]->(i)
create (e)-[:Connected {timeToNode:7}]->(i)
create (e)-[:Connected {timeToNode:3}]->(c)
create (a)-[:Connected {timeToNode:2}]->(f)
create (f)-[:Connected {timeToNode:3}]->(g)
create (f)-[:Connected {timeToNode:1}]->(d)
create (g)-[:Connected {timeToNode:2}]->(h)
create (h)-[:Connected {timeToNode:1}]->(i)


MATCH           path = (startNode:StreetCorner)-[:Connected*]->(endNode:StreetCorner)
WHERE           startNode.name="A" AND endNode.name="I"
RETURN          extract(node in nodes(path) | node.name) AS nameOfNodes,
                extract(relationship in relationships(path) | relationship.timeToNode) AS timeToNodes,
                length(path) AS lengthOfPath,
                reduce(accumulatedTime = 0, relationship in relationships(path) | accumulatedTime + relationship.timeToNode) AS totalWeight
ORDER BY        totalWeight ASC

