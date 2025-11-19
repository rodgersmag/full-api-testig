# swagger_client.DefaultApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_blog_post_posts_post**](DefaultApi.md#create_blog_post_posts_post) | **POST** /posts/ | Create a new blog post
[**create_user_users_post**](DefaultApi.md#create_user_users_post) | **POST** /users/ | Create a new user
[**delete_blog_post_posts_post_id_delete**](DefaultApi.md#delete_blog_post_posts_post_id_delete) | **DELETE** /posts/{post_id} | Delete Blog Post
[**delete_user_users_user_id_delete**](DefaultApi.md#delete_user_users_user_id_delete) | **DELETE** /users/{user_id} | Delete User
[**read_blog_post_posts_post_id_get**](DefaultApi.md#read_blog_post_posts_post_id_get) | **GET** /posts/{post_id} | Read Blog Post
[**read_blog_posts_posts_get**](DefaultApi.md#read_blog_posts_posts_get) | **GET** /posts/ | Read Blog Posts
[**read_user_users_user_id_get**](DefaultApi.md#read_user_users_user_id_get) | **GET** /users/{user_id} | Read User
[**read_users_users_get**](DefaultApi.md#read_users_users_get) | **GET** /users/ | Read Users
[**update_blog_post_posts_post_id_patch**](DefaultApi.md#update_blog_post_posts_post_id_patch) | **PATCH** /posts/{post_id} | Update Blog Post
[**update_user_users_user_id_patch**](DefaultApi.md#update_user_users_user_id_patch) | **PATCH** /users/{user_id} | Update User

# **create_blog_post_posts_post**
> create_blog_post_posts_post(body)

Create a new blog post

Create a new blog post.          **Idempotent**: If a post with the same slug already exists, returns that post (200 OK).          **Validation:**     - Title: 1-200 chars, ASCII alphanumeric + basic punctuation     - Slug: 3-100 chars, kebab-case (lowercase-with-hyphens)     - Content: 10-10000 chars

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.BlogPostCreate() # BlogPostCreate | 

try:
    # Create a new blog post
    api_instance.create_blog_post_posts_post(body)
except ApiException as e:
    print("Exception when calling DefaultApi->create_blog_post_posts_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BlogPostCreate**](BlogPostCreate.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_users_post**
> create_user_users_post(body)

Create a new user

Create a new user with the provided details.          **Idempotent**: If a user with the same email already exists, returns the existing user (200 OK).          **Password Requirements:**     - Length: 8-128 characters     - Allowed characters: A-Z, a-z, 0-9, @$!%*?&

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.UserCreate() # UserCreate | 

try:
    # Create a new user
    api_instance.create_user_users_post(body)
except ApiException as e:
    print("Exception when calling DefaultApi->create_user_users_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UserCreate**](UserCreate.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_blog_post_posts_post_id_delete**
> delete_blog_post_posts_post_id_delete(post_id)

Delete Blog Post

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
post_id = NULL # object | 

try:
    # Delete Blog Post
    api_instance.delete_blog_post_posts_post_id_delete(post_id)
except ApiException as e:
    print("Exception when calling DefaultApi->delete_blog_post_posts_post_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **post_id** | [**object**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_users_user_id_delete**
> delete_user_users_user_id_delete(user_id)

Delete User

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
user_id = NULL # object | 

try:
    # Delete User
    api_instance.delete_user_users_user_id_delete(user_id)
except ApiException as e:
    print("Exception when calling DefaultApi->delete_user_users_user_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | [**object**](.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_blog_post_posts_post_id_get**
> BlogPostRead read_blog_post_posts_post_id_get(post_id)

Read Blog Post

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
post_id = NULL # object | 

try:
    # Read Blog Post
    api_response = api_instance.read_blog_post_posts_post_id_get(post_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->read_blog_post_posts_post_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **post_id** | [**object**](.md)|  | 

### Return type

[**BlogPostRead**](BlogPostRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_blog_posts_posts_get**
> object read_blog_posts_posts_get(skip=skip, limit=limit)

Read Blog Posts

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
skip = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # Read Blog Posts
    api_response = api_instance.read_blog_posts_posts_get(skip=skip, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->read_blog_posts_posts_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | [**object**](.md)|  | [optional] [default to 0]
 **limit** | [**object**](.md)|  | [optional] [default to 100]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_user_users_user_id_get**
> UserRead read_user_users_user_id_get(user_id)

Read User

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
user_id = NULL # object | 

try:
    # Read User
    api_response = api_instance.read_user_users_user_id_get(user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->read_user_users_user_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | [**object**](.md)|  | 

### Return type

[**UserRead**](UserRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_users_users_get**
> object read_users_users_get(skip=skip, limit=limit)

Read Users

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
skip = 0 # object |  (optional) (default to 0)
limit = 100 # object |  (optional) (default to 100)

try:
    # Read Users
    api_response = api_instance.read_users_users_get(skip=skip, limit=limit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->read_users_users_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **skip** | [**object**](.md)|  | [optional] [default to 0]
 **limit** | [**object**](.md)|  | [optional] [default to 100]

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_blog_post_posts_post_id_patch**
> BlogPostRead update_blog_post_posts_post_id_patch(body, post_id)

Update Blog Post

Update blog post - NO slug uniqueness check to avoid 409.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.BlogPostUpdate() # BlogPostUpdate | 
post_id = NULL # object | 

try:
    # Update Blog Post
    api_response = api_instance.update_blog_post_posts_post_id_patch(body, post_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->update_blog_post_posts_post_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**BlogPostUpdate**](BlogPostUpdate.md)|  | 
 **post_id** | [**object**](.md)|  | 

### Return type

[**BlogPostRead**](BlogPostRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_users_user_id_patch**
> UserRead update_user_users_user_id_patch(body, user_id)

Update User

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.DefaultApi()
body = swagger_client.UserUpdate() # UserUpdate | 
user_id = NULL # object | 

try:
    # Update User
    api_response = api_instance.update_user_users_user_id_patch(body, user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->update_user_users_user_id_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UserUpdate**](UserUpdate.md)|  | 
 **user_id** | [**object**](.md)|  | 

### Return type

[**UserRead**](UserRead.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

