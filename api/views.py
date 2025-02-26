from django.shortcuts import render,get_object_or_404

from rest_framework.views import APIView

from rest_framework.response import Response

from api.serializers import UserCreationSerializer,ExpenseSerializer

from rest_framework import authentication,permissions

from myapp.models import Expense

from rest_framework import serializers

# Create your views here.


class UserCreateView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance= UserCreationSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)


class ExpenseListCreateView(APIView):
     
     authentication_classes=[authentication.BasicAuthentication]

     permission_classes=[permissions.IsAuthenticated]

     def get(self,request,*args,**kwargs):
         
         qs = Expense.objects.filter(owner=request.user)

         serializer_instance = ExpenseSerializer(qs,many=True)

         return Response(data=serializer_instance.data)
         


     def post(self,request,*args,**kwargs):

        serializer_instance= ExpenseSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)
        

class ExpenseRetrieveUpdateDestroyView(APIView):

    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def get(self,request,*args,**kwargs):
          
        id=kwargs.get("pk")

        qs=get_object_or_404(Expense,id=id)

        if qs.owner!=request.user:

            raise serializers.ValidationError("you don't have permission")

        serializer_instance=ExpenseSerializer(qs)  #serialization

        return Response(serializer_instance.data)
    

    def delete(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_instance=get_object_or_404(Expense,id=id)

        if expense_instance.owner!=request.user:

            raise serializers.ValidationError("you don't have permission")

        expense_instance.delete()

        return Response(data={"message":"deleted"})
    

    def put(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_instance=get_object_or_404(Expense,id=id)

        if expense_instance.owner!=request.user:

            raise serializers.ValidationError("you don't have permission")

        serializer_instance=ExpenseSerializer(data=request.data,instance=expense_instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)

