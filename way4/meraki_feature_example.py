import meraki

API_KEY = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'

dashboard = meraki.DashboardAPI(API_KEY)

organization_id = '681155'

response = dashboard.organizations.getOrganizationDevices(
    organization_id, total_pages='all'
)

print(response)
