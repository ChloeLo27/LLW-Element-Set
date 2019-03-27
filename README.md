# LLW-Element-Set
A Python implementation of LLW Element Set following a hybrid approach that allows time travel.

## Hybrid Approach?  What?
[LLW Element Set](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type#LWW-Element-Set_(Last-Write-Wins-Element-Set)) is a kind of [Conflict-free replicated data type](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type) (abv. CRDT).  It allows multiple copies to finally sync up and agree with each other at the end.  Most implementations are either a) state based or b) operation based.

For state based implementation, only the final timestamp is stored for each element in both add set and remove set for each LWW Element Set.  While for operation based, any add or remove operation is recorded in the set.  So if an element is repeatedly added to and removed from the set, there will be multiple entries of the element along with the operation timestamp stored inside the set.

Both implementations guarantee eventual convergence among all sets, but state based implementation requires smaller storage space while operation based implementation allows recreation of the set at any given timestamp.  While most applications of CRDT do not require a complete replay of whole history, in some it may be a useful or even necessary feature.  For example, we may think of a multi-device service that syncs the edits to the same document which allows reverting to a particular version in a specific point of time.

Operation based implementaion allows us to revert the set to a given time in history, but it takes up many disk space.  A new hybrid approach that sits in between state based and opetation based implementation will offer a solution to this dilemma.

## Who Cares?
I don't know.  But if you like what I do, feel free to take it and use it.

## But Why?
I originally encountered this problem in a technical challenge.  I got some feedbacks but I do not think they are adequate and to the point.  So this is my attempt to show my true colour and in the hope that I will create something useful.

I also have many free time in my hands, so why not?
