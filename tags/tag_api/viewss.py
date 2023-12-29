from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django import forms
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from rest_framework.views import APIView
from django.db.models import Q
import json
from django.utils.translation import gettext as _

from .models import TagsModel, VM, UserProfile
from .forms import tags_form, VMForm

class Tags(APIView):
    """
    API view for handling CRUD operations on Tags.

    Methods:
    - get: Retrieve tags based on specified filters.
    - post: Create a new tag.
    - delete: Delete a tag if conditions are met.

    """

    def get(self, request):
        """
        Retrieve tags based on specified filters.

        This method handles GET requests to retrieve tags based on optional filters such as tag_id, tag_name, scope, and user_id.

        Parameters:
        - tag_id (optional): Filter tags by tag_id.
        - tag_name (optional): Filter tags by tag_name.
        - scope (optional): Filter tags by scope.
        - user_id (optional): Filter tags by user_id.

        """
        try:
            # Initialize filters for database queries
            filters = Q()

            # Check if tag_id is present in the request and add it to filters
            if request.method == 'GET' and 'tag_id' in request.GET:
                tag_id = request.GET['tag_id']
                filters &= Q(tag_id=tag_id)

            # Check if tag_name is present in the request and add it to filters
            if request.method == 'GET' and 'tag_name' in request.GET:
                tag_name = request.GET['tag_name']
                filters &= Q(tag_name=tag_name)

            # Check if scope is present in the request and add it to filters
            if request.method == 'GET' and 'scope' in request.GET:
                scope = request.GET['scope']
                filters &= Q(scope=scope)

            # Check if user_id is present in the request and add it to filters
            if request.method == 'GET' and 'user_id' in request.GET:
                user_id = request.GET['user_id']
                filters &= Q(user_id=user_id)

            # If no filters, get all tags data, else filter tags based on criteria
            if not filters:
                tags_data = TagsModel.objects.all().values()
            else:
                tags_data = TagsModel.objects.filter(filters).values()

            # Convert queryset to list for JsonResponse
            list_result = [entry for entry in tags_data]

            # Prepare and return JsonResponse
            data = {'status': 'success', 'error_code': 0, 'message': _("Tags get successfully"), 'data': list_result}
            return JsonResponse(data)

        except ValidationError as e:
            # Handle validation error
            data = {'status': 'error', 'error_code': 103, 'message': "error: {0} ".format(e)}
            return JsonResponse(data)

        except NameError as e:
            # Handle name error
            data = {'status': 'error', 'error_code': 103, 'message': "error: {0} ".format(e)}
            return JsonResponse(data)


    def post(self, request):
        """
        Create a new tag.

        This method handles POST requests to create a new tag. It expects the following parameters
        in the POST data:
        - tag_name: Name of the tag
        - scope: Tag scope
        - user_id: User ID associated with the tag
        
        """
        try:
            # Validate the form data
            form = tags_form(request.POST)

            if form.is_valid():
                # Get tag_name, scope, and user_id from the POST data
                tag_name = request.POST.get('tag_name', default=None)
                scope = request.POST.get('scope', default=None)
                user_id = request.POST.get('user_id')

                # Get user profile associated with the provided user_id
                user_profile = get_object_or_404(UserProfile, user_id=user_id)

                # Create a new TagsModel instance
                tag = TagsModel()
                tag.tag_name = tag_name
                tag.scope = scope
                tag.user_id = user_profile

                # Save the tag to the database
                tag_data = tag.save()

                # Prepare and return JsonResponse
                data = {'status': 'success', 'error_code': 0, 'message': _("Tag Added successfully"), 'data': ''}
                return JsonResponse(data)

        except ValidationError as e:
            # Handle validation error
            data = {'status': 'error', 'error_code': 103, 'message': "error: {0} ".format(e)}
            return JsonResponse(data)

        except NameError as e:
            # Handle name error
            data = {'status': 'error', 'error_code': 103, 'message': "error: {0} ".format(e)}
            return JsonResponse(data)

        except IntegrityError:
            # Handle the case of a duplicate tag name
            data = {'status': 'error', 'error_code': 102, 'message': _("This Tag Already exist")}
            return JsonResponse(data)


    def delete(self, request):
        """
        Delete a tag if conditions are met.

        This method handles DELETE requests to delete a tag. It expects the following parameters
        in the request:
        - tag_id: ID of the tag to be deleted
        - user_id: User ID making the request

        """
        try:
            # Get tag_id and user_id from the request parameters
            tag_id = request.GET.get('tag_id')
            user_id = request.GET.get('user_id')

            # Check if tag_id is provided
            if tag_id == None or tag_id == 'None' or tag_id == '':
                data = {'status': 'error', 'error_code': 100, 'message': _('Tag id is required')}
                return JsonResponse(data)

            # Check if user_id is provided
            if user_id == None or user_id == 'None' or user_id == '':
                data = {'status': 'error', 'error_code': 400, 'message': _("User id is required")}
                return JsonResponse(data)

            # Check if the tag is assigned to any VMs
            is_assigned = TagsModel.objects.filter(tag_id=tag_id, vms__isnull=False).exists()

            if is_assigned:
                data = {'status': 'error', 'error_code': 101,
                        'message': _("Tag is assigned to VMs. Unassign it before deleting.")}
                return JsonResponse(data)

            # Check if the user is admin or if the tag was created by the user
            is_admin = user_id == '1'
            is_exist = TagsModel.objects.filter(tag_id=tag_id, user_id__user_id=user_id).count()

            if is_admin or is_exist > 0:
                delete_tag = TagsModel.objects.filter(tag_id=tag_id).delete()
                data = {'status': 'success', 'error_code': 0, 'message': _("Tag deleted successfully.")}
                return JsonResponse(data)
            else:
                data = {'status': 'error', 'error_code': 100, 'message': _("Invalid Request.")}
                return JsonResponse(data)

        except NameError as e:
            # Handle NameError
            data = {'status': 'error', 'error_code': 103, 'message': "error: {0} ".format(e)}
            return JsonResponse(data)

        except KeyError as e:
            # Handle KeyError
            data = {'status': 'error', 'error_code': 102, 'message': "error: {0} is required".format(e)}
            return JsonResponse(data)

        except Exception as e:
            # Handle other exceptions
            data = {'status': 'error', 'error_code': 101, 'message': "error: {0}".format(e)}
            return JsonResponse(data)


# =====================================================================================================  
        
class AssignUnassignTags(APIView):
    def post(self, request):
        """
        Assign or unassign tags to/from objects.

        This method handles POST requests to assign or unassign tags to/from objects.
        It expects the following parameters in the request data:
        - action: 'assign' or 'unassign'
        - tag_name: Name of the tag
        - vm_ids: List of VM IDs to which the tag should be assigned or unassigned

        """
        try:
            # Get the action from the request data
            action = request.data.get("action")

            if action == 'assign':
                # Assign tags to objects
                tag_name = request.data.get('tag_name')
                vm_ids = request.data.get('vm_ids', [])

                # Get the tag instance
                tag = get_object_or_404(TagsModel, tag_name=tag_name)

                # Add the tag to the specified VMs
                tag.vms.add(*vm_ids)

                data = {'status': 'success', 'error_code': 0, 'message': _("Tag Assigned to Objects successfully"), 'data': ''}
                return JsonResponse(data)

            elif action == 'unassign':
                # Unassign tags from objects
                tag_name = request.data.get('tag_name')
                vm_ids = request.data.get('vm_ids', [])

                # Get the tag instance
                tag = get_object_or_404(TagsModel, tag_name=tag_name)

                # Remove the tag from the specified VMs
                tag.vms.remove(*vm_ids)

                data = {'status': 'success', 'error_code': 0, 'message': _("Tag Unassigned from Objects successfully"), 'data': ''}
                return JsonResponse(data)

            else:
                # Invalid action
                data = {'status': 'error', 'error_code': 108, 'message': _("Invalid action")}
                return JsonResponse(data)

        except ValidationError as e:
            # Handle ValidationError
            data = {'status': 'error', 'error_code': 103, 'message': "error: {0} ".format(e)}
            return JsonResponse(data)

        except Exception as e:
            # Handle other exceptions
            data = {'status': 'error', 'error_code': 101, 'message': "error: {0}".format(e)}
            return JsonResponse(data)


# =====================================================================================================  
        

class VMs(APIView):
    def get(self, request):
        """
        Retrieve VMs based on specified filters.

        This method handles GET requests to retrieve a list of Virtual Machines (VMs) based on optional filters. 
        Filters can include tag_name and scope to narrow down the selection.

        Parameters:
        - tag_name (optional): Filter VMs by the specified tag name.
        - scope (optional): Filter VMs by the specified tag scope.

        """
        try:
            tag_name = request.GET.get('tag_name')
            scope = request.GET.get('scope')

            queryset = VM.objects.all()

            if tag_name:
                # Filter VMs by tag name
                queryset = queryset.filter(tags__tag_name=tag_name)

            if scope:
                # Filter VMs by tag scope
                queryset = queryset.filter(tags__scope=scope)

            vm_data = queryset.values()
            vm_list_result = [entry for entry in vm_data]

            data = {'status': 'success', 'error_code': 0, 'message': _("VMs retrieved successfully"), 'data': vm_list_result}
            return JsonResponse(data)
        
        except Exception as e:
            # Handle any unexpected errors
            data = {'status': 'error', 'error_code': 101, 'message': f"Error: {e}"}
            return JsonResponse(data)
        

    def post(self, request):
        """
        Create a new Virtual Machine (VM) instance.

        This method handles POST requests to create a new VM. It expects the following parameters
        in the request data:
        - vm_name: Name of the VM.
        - tags (optional): Name of the tag to associate with the VM.
        - scope (optional): Scope of the tag associated with the VM.
        - user_id: User ID associated with the VM.

        The method checks for the existence of a VM with the same name and creates a new VM instance if it doesn't exist.
        It also associates the VM with a tag if provided or creates a new tag.

        """
        try:
            form = VMForm(request.POST)

            vm_name = request.POST.get('vm_name')
            tag_name = request.POST.get('tags')
            scope = request.POST.get('scope')
            user_id = request.POST.get('user_id')

            # Check if VM instance with the same name already exists
            existing_vm = VM.objects.filter(vm_name=vm_name).exists()

            if existing_vm:
                data = {'status': 'error', 'error_code': 102, 'message': _("This VM Already exist.")}
                return JsonResponse(data)

            # Get or create the VM instance
            vm_instance = VM.objects.create(vm_name=vm_name)

            if tag_name:
                user_profile = get_object_or_404(UserProfile, user_id=user_id)

                # Try to get the existing tag
                tag_instance = TagsModel.objects.filter(tag_name=tag_name, scope=scope).first()

                if tag_instance is None:
                    tag_instance = TagsModel.objects.create(tag_name=tag_name, scope=scope, user_id=user_profile)

                # Assign the tag to the VM instance
                vm_instance.tags.add(tag_instance)

            data = {'status': 'success', 'error_code': 0, 'message': _("VM added successfully."), 'data': ''}
            return JsonResponse(data)
        
        except Exception as e:
            # Handle any unexpected errors
            data = {'status': 'error', 'error_code': 101, 'message': f"Error: {e}"}
            return JsonResponse(data)


    def put(self, request):
        """
        Update an existing Virtual Machine (VM) with new information.

        This method handles PUT requests to update an existing VM with new data. The request data should include
        the following parameters:
        - id: ID of the VM to be updated.
        - vm_name (optional): New name for the VM.
        - tags (optional): List of tag IDs to be associated with the VM.

        The method retrieves the existing VM instance based on the provided ID, validates the new data using a form,
        and then updates the VM with the new information. It specifically updates the VM's name and associated tags.
        If the provided tag IDs include existing tags, they will be associated with the VM.

        """
        try:
            vm_instance = VM.objects.get(id=request.data.get('id'))
            form = VMForm(request.data, instance=vm_instance)

            if form.is_valid():
                # Save VM without committing to the database
                updated_vm_instance = form.save(commit=False)

                # Get tag IDs from the request
                tag_ids = request.data.getlist('tags')

                # Assign tags to the updated VM instance
                updated_vm_instance.tags.set(tag_ids)

                # Save the updated VM instance to the database
                updated_vm_instance.save()

                data = {'status': 'success', 'error_code': 0, 'message': _("VM updated successfully"), 'data': ''}
                return JsonResponse(data)
            else:
                # Validation error in the form
                data = {'status': 'error', 'error_code': 103, 'message': f"Validation Error: {form.errors}"}
                return JsonResponse(data)

        except VM.DoesNotExist:
            # VM with the provided ID not found
            data = {'status': 'error', 'error_code': 100, 'message': _("VM not found")}
            return JsonResponse(data)

        except Exception as e:
            # Handle any unexpected errors
            data = {'status': 'error', 'error_code': 101, 'message': f"Error: {e}"}
            return JsonResponse(data)


    def delete(self, request, vm_id):
        """
        Delete a Virtual Machine (VM) based on the provided ID.

        This method handles DELETE requests to delete a VM with the specified ID.
        
        Parameters (in URL):
        - vm_id: ID of the VM to be deleted.

        """
        try:
            vm = VM.objects.get(id=vm_id)
            vm.delete()

            data = {'status': 'success', 'error_code': 0, 'message': _("VM deleted successfully")}
            return JsonResponse(data)

        except VM.DoesNotExist:
            # VM with the provided ID not found
            data = {'status': 'error', 'error_code': 100, 'message': _("VM not found")}
            return JsonResponse(data)

        except Exception as e:
            # Handle any unexpected errors
            data = {'status': 'error', 'error_code': 101, 'message': f"Error: {e}"}
            return JsonResponse(data)

# ==============================================================================

class Users(APIView):
    def get(self, request):
        
        user_data = UserProfile.objects.all()

        users = [{'user_id': user.user_id, 'user_name': user.user_name} for user in user_data]

        return JsonResponse({'users': users})