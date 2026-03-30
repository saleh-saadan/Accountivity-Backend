from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import TDList, Task

User = get_user_model()


class MemberSerializer(serializers.ModelSerializer):
    """
    Sends user_id and username to front-end
    """
    class Meta:
        model = User
        fields = ("user_id", "username")


class TaskSerializer(serializers.ModelSerializer):
    """
    Receives name of task and id of list from front-end
    Sends task id, name, creator id, list id, completed, and created to front-end
    """
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = ("id", "name", "creator", "list", "completed", "created")
        read_only_fields = ("creator", "completed", "created")

    def create(self, validated_data):
        """
        Assign user as creator when creating task
        """

        task = Task.objects.create(
            creator=self.context["request"].user, **validated_data
        )

        return task


class UpdateTaskSerializer(serializers.Serializer):
    """
    Receives task_id and updated name or completed from front-end
    """

    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), source="task"
    )
    name = serializers.CharField(required=False)
    completed = serializers.BooleanField(required=False)


class TDListSerializer(serializers.ModelSerializer):
    """
    Receives name and user_id of members from front-end
    Sends id, name, member_info (output from MemberSerializer) and tasks to front-end
    """

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True
    )
    member_info = MemberSerializer(read_only=True, many=True, source="members")
    tasks = TaskSerializer(read_only=True, many=True, source="tasks")

    class Meta:
        model = TDList
        fields = ("id", "name", "members", "member_info", "tasks")

    def create(self, validated_data):
        """
        Extract list of members and assign them after list 
        has been created (and assign the user as creator during creation)
        """

        members = validated_data.pop("members", [])

        td_list = TDList.objects.create(
            creator=self.context["request"].user, **validated_data
        )
        td_list.members.set(members)

        return td_list


class UpdateTDListSerializer(serializers.Serializer):
    """
    Receives list_id and updated list name 
    or id of members to add/remove from front-end
    """

    list_id = serializers.PrimaryKeyRelatedField(
        queryset=TDList.objects.all(), source="list"
    )
    name = serializers.CharField(required=False)
    add_members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )
    remove_members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )
